#!/usr/bin/perl
use Modern::Perl;
use Dancer;
use Data::Dumper qw<Dumper>;
use Thetical::Battle::Map;
use Thetical::Battle::Move;
use Thetical::Battle::Attack;
use Thetical::Battle::Character;
set 'session'     => 'Simple';
set 'logger'      => 'console';
set 'log'         => 'debug';
set 'show_errors' => 1;
set 'access_log'  => 1;
set 'warnings'    => 1;

before sub {
    unless ( session('chars') ) {

        session chars => {'11' => { 'id'        => 11
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

        session map => Thetical::Battle::Map::Load( 'demo' );

    }
};

# Decrements all characters CT until a CT hits 0
sub getnextactive {
    my $chars = session('chars');

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
                session chars => $chars;
                last CT;
            }
        }
    }
}

# Returns the whole map
get '/map' => sub {
    getnextactive; # Decrements all characters CT until a CT hits 0
    to_json session('map');
};

# Returns character stats
get '/char/:id' => sub {
    my $chars = session('chars');
    to_json $$chars{ params->{id} };
};

# Returns the list of walkable tiles for a character
get '/char/:id/walkables' => sub {
    my $map   = session('map');
    my $chars = session('chars');
    my $char  = $$chars{ params->{id} };
    to_json Thetical::Battle::Move::GetWalkables( $map, $char );
};

# Returns the list of attackables tiles for a character
get '/char/:id/attackables' => sub {
    my $map   = session('map');
    my $chars = session('chars');
    my $char  = $$chars{ params->{id} };
    to_json Thetical::Battle::Attack::GetAttackables( $map, $char );
};

# Move action
get '/char/:id/moveto/:y/:x' => sub {
    my $id = params->{id};
    my $y2 = params->{y};
    my $x2 = params->{x};

    my $map   = session('map');
    my $chars = session('chars');
    my $char  = $$chars{$id};

    # permissions checks
    send_error("Not allowed", 403) unless defined $$char{active} && $$char{active} == 1;
    send_error("Not allowed", 403) unless Thetical::Battle::Move::IsWalkable( $map, $char, $y2, $x2 );

    # get actual coordinates
    my $tile = Thetical::Battle::Character::Coords( $map, $char );
    my $y1 = $tile->[0];
    my $x1 = $tile->[1];

    # get path to return before switching positions
    my $path = Thetical::Battle::Move::GetPath( $map, $char, $y1, $x1, $y2, $x2 );

    # switch positions
    $$map{tiles}[$y1][$x1]{char} = 0;
    $$map{tiles}[$y2][$x2]{char} = $id;

    # set new direction and remove the ability to walk for this turn
    $$char{direction} = Thetical::Battle::Move::GetNewDirection( $y1, $x1, $y2, $x2 );
    $$char{canmove} = 0;

    # save changes
    session map   => $map;
    session chars => $chars;

    return to_json $path;
};

# Wait action: this is where charecter's turn ends
get '/char/:id/wait/:direction' => sub {
    my $id = params->{id};
    
    # permissions checks
    my $chars = session('chars');
    my $char = $$chars{$id};
    send_error("Not allowed", 403) unless $$char{active} == 1;
    
    # the character conserves half of his CT
    # if Move or Act has not be consumed
    $$char{ct} = $$char{canmove}
               | $$char{canact} 
               ? int( $$char{ctmax} / 2 )
               : $$char{ctmax};
    
    # set the character direction
    $$char{direction} = params->{direction};
    
    # end of this character's turn
    $$char{active } = 0;
    $$char{canmove} = 0;
    $$char{canact } = 0;

    # save changes
    session chars => $chars;
    
    return 1;
};

# Attack action
get '/char/:id1/attack/:id2' => sub {
    my $id1 = params->{id1};
    my $id2 = params->{id2};
    
    my $chars = session('chars');
    my $char1 = $$chars{$id1};
    my $char2 = $$chars{$id2};
    
    send_error("Not allowed", 403) unless $$char1{active} == 1;
    
    $$char2{hp} -= 5;
    $$char2{hp} = 0 if $$char2{hp} < 0;
    
    $$char1{canact} = 0;
    
    session chars => $chars;
    
    return 5;
};

dance;
