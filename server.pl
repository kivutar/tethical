#!/usr/bin/perl
use Modern::Perl;
use Dancer;
use Data::Dumper qw<Dumper>;
logger 'console';

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

sub getcharcoords {
    my $id = shift;

    for my $y ( 0..$$map{height}-1 ) {
        for my $x ( 0..$$map{width}-1 ) {

            my $tile = $$map{tiles}[$y][$x];
            if ( defined $$tile{char} && $$tile{char} == $id ) {
                return [$y, $x];
            }
        }
    }
}

my $chars = { '11' => { 'hp'    => 10
                      , 'hpmax' => 10
                      , 'ct'    => 12
                      , 'ctmax' => 12
                      , 'team'  => 1
                      , 'move'  => 5
                      , 'direction' => 1 }
            , '12' => { 'hp'    => 15
                      , 'hpmax' => 15
                      , 'ct'    => 10
                      , 'ctmax' => 10
                      , 'team'  => 1
                      , 'move'  => 4
                      , 'direction' => 1 }
            , '13' => { 'hp'    => 12
                      , 'hpmax' => 12
                      , 'ct'    => 11
                      , 'ctmax' => 11
                      , 'team'  => 1
                      , 'move'  => 6
                      , 'direction' => 1 }
            , '14' => { 'hp'    => 13
                      , 'hpmax' => 13
                      , 'ct'    => 13
                      , 'ctmax' => 13
                      , 'team'  => 1
                      , 'move'  => 5
                      , 'direction' => 1 }
            , '21' => { 'hp'    => 10
                      , 'hpmax' => 10
                      , 'ct'    => 12
                      , 'ctmax' => 12
                      , 'team'  => 2
                      , 'move'  => 5
                      , 'direction' => 0 }
            , '22' => { 'hp'    => 15
                      , 'hpmax' => 15
                      , 'ct'    => 10
                      , 'ctmax' => 10
                      , 'team'  => 2
                      , 'move'  => 4
                      , 'direction' => 0 }
            , '23' => { 'hp'    => 12
                      , 'hpmax' => 12
                      , 'ct'    => 11
                      , 'ctmax' => 11
                      , 'team'  => 2
                      , 'move'  => 6
                      , 'direction' => 0 }
            , '24' => { 'hp'    => 13
                      , 'hpmax' => 13
                      , 'ct'    => 13
                      , 'ctmax' => 13
                      , 'team'  => 2
                      , 'move'  => 5
                      , 'direction' => 0 }
};

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

get '/map' => sub {
    getnextactive;
    to_json $map;
};

get '/char/:id' => sub {
    to_json $$chars{ params->{id} };
};

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

sub getwalkables {
    my $id = shift;
    my $char = $$chars{$id};
    my $tile = getcharcoords $id;
    my @walkables = ( $tile );
    
    for ( 1..$$char{move} ) {
        push @walkables, getadjacentwalkables( @walkables );
    }
    
    @walkables = map { $_->[0] == $tile->[0] && $_->[1] == $tile->[1] ? () : $_ } @walkables;

    return \@walkables;
}

sub is_walkable {
    my ($id, $y, $x) = @_;

    my $walkables = getwalkables($id);

    for ( @$walkables ) {
        return 1 if $y == $_->[0] && $x == $_->[1];
    }

    undef;
}

get '/char/:id/walkables' => sub {
    to_json getwalkables params->{id};
};

sub getnewdirection {
    my ($y1, $x1, $y2, $x2) = @_;

    my $dy = $y2 - $y1;
    my $dx = $x2 - $x1;
    if ( $dy*$dy > $dx*$dx ) {
        return $dy > 0 ? 1 : 0;
    } else {
        return $dx > 0 ? 2 : 3;
    }
}

get '/char/:id/moveto/:y/:x' => sub {
    my $id = params->{id};
    my $y2  = params->{y};
    my $x2  = params->{x};

    if ( is_walkable($id, $y2, $x2) ) {
        my $tile = getcharcoords $id;
        my $y1 = $tile->[0];
        my $x1 = $tile->[1];

        $$map{tiles}[$y1][$x1]{char} = 0;
        $$map{tiles}[$y2][$x2]{char} = $id;

        $$chars{$id}{direction} = getnewdirection($y1, $x1, $y2, $x2);
        $$chars{$id}{active} = 0;
        $$chars{$id}{canmove} = 0;
        $$chars{$id}{canact} = 0;
        $$chars{$id}{ct} = $$chars{$id}{ctmax};
        return 1;
    } else {
        send_error("Not allowed", 403);
    }
};

dance;
