#!/usr/bin/perl
use Modern::Perl;
use Dancer;
use Data::Dumper qw<Dumper>;
use Thetical::Battle::Map;
use Thetical::Battle::Move;
use Thetical::Battle::Character;
set session => 'YAML';
logger 'console';

my $map = Thetical::Battle::Map::Load( 'demo' );

# Decrements all characters CT until a CT hits 0
sub getnextactive {
    for my $id ( keys %{ Thetical::Battle::Character::List() } ) {
        my $char = Thetical::Battle::Character::Get( $id );
        return if defined $$char{active} && $$char{active} == 1;
    }

    CT: while ( 1 ) {
        for my $id ( keys %{ Thetical::Battle::Character::List() } ) {
            my $char = Thetical::Battle::Character::Get( $id );
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
    to_json Thetical::Battle::Character::Get(  params->{id} );
};

# Returns the list of walkable tiles for a character
get '/char/:id/walkables' => sub {
    to_json Thetical::Battle::Move::getwalkables( params->{id}, $map );
};

# Move action
get '/char/:id/moveto/:y/:x' => sub {

    my $id = params->{id};
    my $y2 = params->{y};
    my $x2 = params->{x};

    # permissions checks
    my $char = Thetical::Battle::Character::Get( $id );
    return unless $$char{active} == 1;

    # check if the character can walk to the requested position
    if ( Thetical::Battle::Move::is_walkable( $id, $y2, $x2 ) ) {

        # get actual coordinates
        my $tile = Thetical::Battle::Character::getcharcoords( $id, $map );
        my $y1 = $tile->[0];
        my $x1 = $tile->[1];

        # switch positions
        $$map{tiles}[$y1][$x1]{char} = 0;
        $$map{tiles}[$y2][$x2]{char} = $id;

        # set new direction and remove the ability to walk for this turn
        $$char{direction} = Thetical::Battle::Move::getnewdirection( $y1, $x1, $y2, $x2 );
        $$char{canmove} = 0;
        return to_json Thetical::Battle::Move::getpath( $id, $y1, $x1, $y2, $x2 );

    } else {
        send_error("Not allowed", 403);
    }
};

# Wait action: this is where charecter's turn ends
get '/char/:id/wait/:direction' => sub {
    my $id = params->{id};
    
    # permissions checks
    my $char = Thetical::Battle::Character::Get( $id );
    return unless $$char{active} == 1;
    
    # the character conserves half of his CT
    # if Move or Act has not be consumed
    $$char{ct} = $$char{canmove}
               | $$char{canact} 
               ? $$char{ctmax} / 2 
               : $$char{ctmax};
    
    # set the character direction
    $$char{direction} = params->{direction};
    
    # end of this character's turn
    $$char{active} = 0;
    $$char{canmove} = 0;
    $$char{canact} = 0;
    
    return 1;
};

dance;
