#!/usr/bin/perl
use Modern::Perl;
use Dancer;
use Data::Dumper qw<Dumper>;
logger 'console';

# Open the map files, and return the map data structure
sub loadmap {
    my $name = shift;
    my $map = {};
    
    for my $layer ( qw<heights chars walkables ground> ) {
        open FH, "maps/$name.$layer";
        $$map{$layer} = [ map { chomp $_; [ split /,/ ] } <FH> ];
        close FH;
    }
    
    my $height = @{$$map{heights}};
    my $width  = @{$$map{heights}[0]};
    
    my $map2 = { name   => $name
               , height => $height
               , width  => $width };
    
    for my $y (0..$height-1) {
        for my $x (0..$width-1) {

            $$map2{tiles}[$y][$x] = { 'height'   => $$map{heights  }[$y][$x]
                                    , 'char'     => $$map{chars    }[$y][$x]
                                    , 'walkable' => $$map{walkables}[$y][$x]
                                    , 'ground'   => $$map{ground   }[$y][$x] };
        }
    }

    $map2;
}

my $map = loadmap 'demo';

# Returns the coordinates of a character
sub getcharcoords {
    my $id = shift;

    # loop over all the tiles of the map
    for my $y ( 0..$$map{height}-1 ) {
        for my $x ( 0..$$map{width}-1 ) {

            my $tile = $$map{tiles}[$y][$x];
            
            # return tile coordinates when the character is found
            if ( defined $$tile{char} && $$tile{char} == $id ) {
                return [$y, $x];
            }
        }
    }
}

my $chars = { '11' => { 'id'        => 11
                      , 'hp'        => 10
                      , 'hpmax'     => 10
                      , 'ct'        => 12
                      , 'ctmax'     => 12
                      , 'team'      => 1
                      , 'move'      => 5
                      , 'direction' => 1 }
            , '12' => { 'id'        => 12
                      , 'hp'        => 15
                      , 'hpmax'     => 15
                      , 'ct'        => 10
                      , 'ctmax'     => 10
                      , 'team'      => 1
                      , 'move'      => 4
                      , 'direction' => 1 }
            , '13' => { 'id'        => 13
                      , 'hp'        => 12
                      , 'hpmax'     => 12
                      , 'ct'        => 11
                      , 'ctmax'     => 11
                      , 'team'      => 1
                      , 'move'      => 6
                      , 'direction' => 1 }
            , '14' => { 'id'        => 14
                      , 'hp'        => 13
                      , 'hpmax'     => 13
                      , 'ct'        => 13
                      , 'ctmax'     => 13
                      , 'team'      => 1
                      , 'move'      => 5
                      , 'direction' => 1 }
            , '21' => { 'id'        => 21
                      , 'hp'        => 10
                      , 'hpmax'     => 10
                      , 'ct'        => 12
                      , 'ctmax'     => 12
                      , 'team'      => 2
                      , 'move'      => 5
                      , 'direction' => 0 }
            , '22' => { 'id'        => 22
                      , 'hp'        => 15
                      , 'hpmax'     => 15
                      , 'ct'        => 10
                      , 'ctmax'     => 10
                      , 'team'      => 2
                      , 'move'      => 4
                      , 'direction' => 0 }
            , '23' => { 'id'        => 23
                      , 'hp'        => 12
                      , 'hpmax'     => 12
                      , 'ct'        => 11
                      , 'ctmax'     => 11
                      , 'team'      => 2
                      , 'move'      => 6
                      , 'direction' => 0 }
            , '24' => { 'id'        => 24
                      , 'hp'        => 13
                      , 'hpmax'     => 13
                      , 'ct'        => 13
                      , 'ctmax'     => 13
                      , 'team'      => 2
                      , 'move'      => 5
                      , 'direction' => 0 }
};

# Decrements all characters CT until a CT hits 0
sub getnextactive {
    for my $id ( keys %$chars ) {
        my $char = $$chars{$id};
        return if defined $$char{active} && $$char{active} == 1;
    }

    CT: while ( 1 ) {
        for my $id ( keys %$chars ) {
            my $char = $$chars{$id};
            $$char{ct}--;
            if ( $$char{ct} == 0 ) {
                $$char{active}  = 1;
                $$char{canmove} = 1;
                $$char{canact}  = 1;
                last CT;
            }
        }
    }
}

# Returns the whole map
get '/map' => sub {
    getnextactive; # Decrements all characters CT until a CT hits 0
    to_json $map;
};

# Returns character stats
get '/char/:id' => sub {
    to_json $$chars{ params->{id} };
};

# Used in walkable tiles computation
sub getadjacentwalkables {
    my $w2;

    for my $t1 ( @_ ) {
        for my $tx ( ( [$t1->[0]-1, $t1->[1]  ]
                     , [$t1->[0]+1, $t1->[1]  ]
                     , [$t1->[0]  , $t1->[1]-1]
                     , [$t1->[0]  , $t1->[1]+1] ) ) {
            eval {
                my $t2 = $$map{tiles}[$tx->[0]][$tx->[1]];
                if ( $t2 && ! $$t2{char} > 0 ) {
                    push @$w2, [$tx->[0], $tx->[1]];
                }
            };
        }
    }

    @$w2;
}

# Compute the list of walkable tiles for a character
sub getwalkables {
    my $id = shift;
    my $char = $$chars{$id};
    my $tile = getcharcoords $id;
    my @walkables = ( $tile );

    for ( 1..$$char{move} ) {
        push @walkables, getadjacentwalkables( @walkables );
    }

    # Remove character's tile from the list
    @walkables = map { $_->[0] == $tile->[0] && $_->[1] == $tile->[1] ? () : $_ } @walkables;

    return \@walkables;
}

# Used to check if a tile is walkable for a character
sub is_walkable {
    my ($id, $y, $x) = @_;

    my $walkables = getwalkables($id);

    for ( @$walkables ) {
        return 1 if $y == $_->[0] && $x == $_->[1];
    }

    undef;
}

# Returns the list of walkable tiles for a character
get '/char/:id/walkables' => sub {
    to_json getwalkables params->{id};
};

# Returns the character's new direction after a move
# 0 = up, 1 = down, 2 = left, 3 = right
sub getnewdirection {
    my ($y1, $x1, $y2, $x2) = @_;

    # compute the move vector
    my $dy = $y2 - $y1;
    my $dx = $x2 - $x1;
    
    # was the move more hortizontal of vertical ?
    if ( $dy*$dy > $dx*$dx ) {
        return $dy > 0 ? 1 : 0; # up or down ?
    } else {
        return $dx > 0 ? 2 : 3; # left or right ?
    }
}

# Move action
get '/char/:id/moveto/:y/:x' => sub {

    my $id = params->{id};
    my $y2  = params->{y};
    my $x2  = params->{x};

    # permissions checks
    return unless $$chars{$id}{active} == 1;

    # check if the character can walk to the requested position
    if ( is_walkable($id, $y2, $x2) ) {

        # get actual coordinates
        my $tile = getcharcoords $id;
        my $y1 = $tile->[0];
        my $x1 = $tile->[1];

        # switch positions
        $$map{tiles}[$y1][$x1]{char} = 0;
        $$map{tiles}[$y2][$x2]{char} = $id;

        # set new direction and remove the ability to walk for this turn
        $$chars{$id}{direction} = getnewdirection($y1, $x1, $y2, $x2);
        $$chars{$id}{canmove} = 0;
        return 1;

    } else {
        send_error("Not allowed", 403);
    }
};

# Wait action: this is where charecter's turn ends
get '/char/:id/wait/:direction' => sub {
    my $id        = params->{id};
    
    # permissions checks
    return unless $$chars{$id}{active} == 1;
    
    # the character conserves half of his CT
    # if Move or Act has not be consumed
    $$chars{$id}{ct} = $$chars{$id}{canmove}
                     | $$chars{$id}{canact} 
                     ? $$chars{$id}{ctmax} / 2 
                     : $$chars{$id}{ctmax};
    
    # set the character direction
    $$chars{$id}{direction} = params->{direction};
    
    # end of this character's turn
    $$chars{$id}{active} = 0;
    $$chars{$id}{canmove} = 0;
    $$chars{$id}{canact} = 0;
    
    return 1;
};

dance;
