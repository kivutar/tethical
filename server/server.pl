#!/usr/bin/perl
use Modern::Perl;
use Dancer;
use Data::Dumper qw<Dumper>;
use Tethical::Battle::Map;
use Tethical::Battle::Move;
use Tethical::Battle::Attack;
use Tethical::Battle::Character;
set 'session'     => 'Simple';
set 'logger'      => 'console';
set 'log'         => 'debug';
set 'show_errors' => 1;
set 'access_log'  => 1;
set 'warnings'    => 1;

my $players = [];
my $parties = {};

any '/login' => sub {
    return send_error("Already logged in", 403) if session->{loggedin};
    return send_error("Wrong credentials", 403) unless params->{login} eq params->{pass};
    return send_error("Username already in use", 403) if grep { $_ eq params->{login} } @$players;

    push @$players, params->{login};
    session loggedin => 1;
    session login    => params->{login};
    1;
};

any '/logout' => sub {
    return send_error("Not logged in", 403) unless session->{loggedin};
    session loggedin => 0;
    1;
};

get '/parties' => sub {
    return send_error("Not logged in", 403) unless session->{loggedin};
    to_json $parties;
};

post '/ownparty' => sub {
    return send_error("Not logged in", 403) unless session->{loggedin};

    my $name = params->{name};

    my $party = { 'name'    => $name
                , 'mapname' => params->{mapname}
                , 'map'     => Tethical::Battle::Map::Load( params->{mapname} )
                , 'chars'   => {}
                , 'log'     => {}
                , 'creator' => session->{login}
                , 'player1' => session->{login} };
    
    $$parties{$name} = $party;
    session party  => $name;
    session player => 1;
    
    to_json $party;
};

any '/joinparty/:name' => sub {
    return send_error("Not logged in", 403) unless session->{loggedin};

    my $party        = $$parties{params->{name}};
    $$party{player2} = session->{login};
    session party   => params->{name};
    session player  => 2;
    
    to_json $party;
};

get '/party' => sub {
    return send_error("Not logged in", 403) unless session->{loggedin};
    to_json $$parties{ session->{party} };
};

get '/choosechar' => sub {
    return send_error("Not logged in", 403) unless session->{loggedin};

    my $name = session('party');
    my $player = session('player');
    my $party = $$parties{$name};

    return send_error("Party not full", 403) unless $$party{player1} and $$party{player2};

    to_json $$party{'map'}{chartiles}{$player};
};

any '/startbattle' => sub {
    return send_error("Not logged in", 403) unless session->{loggedin};
     
    my $name = session('party');
    my $player = session('player');
    my $party = $$parties{$name};
    
    return send_error("Battle already started", 403) if $player == 1 and $$party{player1started};
    return send_error("Battle already started", 403) if $player == 2 and $$party{player2started};

    my %params = params;
    for my $k ( keys %params ) {
        if ( params->{$k} ) {
            my ($x, $y, $z, $direction) = split '-', $k;
            my $charid  = params->{$k};
            
            $$party{map}{tiles}[$x][$y][$z]{char} = $charid;
            my $char = { 'id'        => $charid
                       , 'name'      => $charid
                       , 'job'       => 'Unknown'
                       , 'sign'      => 1
                       , 'hp'        => 10
                       , 'hpmax'     => 10
                       , 'ct'        => 12
                       , 'ctmax'     => 12
                       , 'team'      => $player
                       , 'move'      => 4
                       , 'direction' => $direction
                       , 'sprite'    => $player eq 1 ? 'misty' : 'ramza'
                       , 'active'    => 0 };
            $$party{chars}{$charid} = $char;
        }
    }

    $$party{player1started} = 1 if $player == 1;
    $$party{player2started} = 1 if $player == 2;

    1;
};

# Decrements all characters CT until a CT hits 0
sub getnextactive {
    my $party = $$parties{session('party')};
    my $chars = $$party{chars};

    for ( keys %$chars ) {
        $$party{yourturn} = $$chars{$_}{team} == session->{player};
        return if $$chars{$_}{active};
    }

    CT: while ( 1 ) {
        for my $id ( keys %$chars ) {
            my $char = $$chars{$id};
            $$char{ct}--;
            if ( $$char{ct} == 0 ) {
                if ( $$char{hp} > 0 ) {
                    $$char{active}  = 1;
                    $$char{canmove} = 1;
                    $$char{canact}  = 1;
                    $$party{yourturn} = $$char{team} == session->{player};
                    last CT;
                } else {
                    $$char{ct} = $$char{ctmax};
                }
            }
        }
    }
}

sub aliveteams {
    my $party = $$parties{session('party')};
    my $chars = $$party{chars};
    #[ map { $$chars{$_}{hp} > 0 ? $$chars{$_} : () } keys %$chars ];

    my %aliveteams;

    for ( keys %$chars ) {
        $aliveteams{$$chars{$_}{team}}++ if $$chars{$_}{hp} > 0;
    }

    scalar keys %aliveteams;
}

# Battle main callback
get '/battle' => sub {
    return send_error("Not logged in", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Party not started for all players", 403) unless $$party{player1started} and $$party{player2started};
    $$party{log} = { 'act' => 'end' } if aliveteams == 1;
    getnextactive;
    to_json $party;
};

# Returns character stats
get '/char/:id' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};
    to_json $$party{chars}{ params->{id} };
};

# Returns the list of walkable tiles for a character
get '/char/:id/walkables' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};
    my $map   = $$party{map};
    my $char  = $$party{chars}{ params->{id} };
    to_json Tethical::Battle::Move::GetWalkables( $map, $char );
};

# Returns the list of attackables tiles for a character
get '/char/:id/attackables' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};
    my $map   = $$party{map};
    my $char  = $$party{chars}{ params->{id} };
    to_json Tethical::Battle::Attack::GetAttackables( $map, $char );
};

# Get path from tile to tile
get '/char/:id/path/:x/:y/:z' => sub {
    return send_error("Not logged in", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not in a started party", 403) unless $$party{player1started} and $$party{player2started};

    my $id = params->{id};
    my $x2 = params->{x};
    my $y2 = params->{y};
    my $z2 = params->{z};

    my $map   = $$party{map};
    my $char  = $$party{chars}{ params->{id} };

    # permissions checks
    return send_error("Not this character's turn",             403) unless $$char{active} == 1;
    return send_error("Tile not walkable",                     403) unless Tethical::Battle::Move::IsWalkable( $map, $char, $x2, $y2, $z2 );
    return send_error("This character does not belong to you", 403) unless $$char{team} == session->{player};

    # get actual coordinates
    my $tile = Tethical::Battle::Character::Coords( $map, $char );
    my $x1 = $tile->[0];
    my $y1 = $tile->[1];
    my $z1 = $tile->[2];

    my $path = Tethical::Battle::Move::GetPath( $map, $char, $x1, $y1, $z1, $x2, $y2, $z2 );

    return to_json $path;
};

# Move action
get '/char/:id/moveto/:x/:y/:z' => sub {
    return send_error("Not logged in", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not in a started party", 403) unless $$party{player1started} and $$party{player2started};

    my $id = params->{id};
    my $x2 = params->{x};
    my $y2 = params->{y};
    my $z2 = params->{z};

    my $map   = $$party{map};
    my $char  = $$party{chars}{ params->{id} };

    # permissions checks
    return send_error("Not this character's turn",             403) unless $$char{active} == 1;
    return send_error("Tile not walkable",                     403) unless Tethical::Battle::Move::IsWalkable( $map, $char, $x2, $y2, $z2 );
    return send_error("This character does not belong to you", 403) unless $$char{team} == session->{player};
    return send_error("This character can't move",             403) unless $$char{canmove};

    # get actual coordinates
    my $tile = Tethical::Battle::Character::Coords( $map, $char );
    my $x1 = $tile->[0];
    my $y1 = $tile->[1];
    my $z1 = $tile->[2];
    
    # get walkables and path to log before switching positions
    my $path = Tethical::Battle::Move::GetPath( $map, $char, $x1, $y1, $z1, $x2, $y2, $z2 );
    my $walkables = Tethical::Battle::Move::GetWalkables( $map, $char );

    # switch positions
    $$map{tiles}[$x1][$y1][$z1]{char} = 0;
    $$map{tiles}[$x2][$y2][$z2]{char} = $id;

    # set new direction and remove the ability to walk for this turn
    $$char{direction} = Tethical::Battle::Move::GetNewDirection( $x1, $y1, $x2, $y2 );
    $$char{canmove} = 0;
    
    $$party{log} = { act => 'move', charid => $id, walkables => $walkables, path => $path };

    1;
};

# Wait action: this is where charecter's turn ends
get '/char/:id/wait/:direction' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};

    my $id = params->{id};
    
    # permissions checks
    my $char = $$party{chars}{$id};
    return send_error("Not allowed", 403) unless $$char{active} == 1;
    return send_error("Not allowed", 403) unless $$char{team} == session->{player};
    
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
    
    $$party{log} = { act => 'wait', charid => $id, direction => $$char{direction} };
    
    return 1;
};

# Attack action
get '/char/:id1/attack/:id2' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};

    my $id1 = params->{id1};
    my $id2 = params->{id2};
    
    my $map   = $$party{map};
    my $chars = $$party{chars};
    my $char1 = $$chars{$id1};
    my $char2 = $$chars{$id2};
    
    return send_error("Not this character's turn",             403) unless $$char1{active} == 1;
    return send_error("Tile not attackable",                   403) unless Tethical::Battle::Attack::IsAttackable( $map, $char1, $char2 );
    return send_error("This character does not belong to you", 403) unless $$char1{team} == session->{player};
    return send_error("This character can't act",              403) unless $$char1{canact};
    
    my $damages = 3;
    
    $$char2{hp} -= $damages;
    $$char2{hp} = 0 if $$char2{hp} < 0;
    
    $$char1{canact} = 0;
    
    my $attackables = Tethical::Battle::Attack::GetAttackables( $map, $char1 );
    
    $$party{log} = { act => 'attack', charid => $id1, targetid => $id2, damages => $damages, attackables => $attackables };
    
    return $damages;
};

# Get actions performed by the other players
get '/otherplayers' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};

    my $log = $$party{log};
    $$party{log} = {};

    return to_json $log;
};

dance;
