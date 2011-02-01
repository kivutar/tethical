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

my $parties = {};

get '/' => sub {
    if ( session('loggedin') ) {
        redirect '/parties';
    } else {
        return '
        <h1>Tethical</h1>
        <form method="post" action="/login">
            <fieldset>
                <legend>Login</legend>
                <p><strong>Login: </strong><input type="text" name="login" /></p>
                <p><strong>Pass: </strong><input type="password" name="pass" /></p>
                <p><input type="submit" value="Login" /></p>
            </fieldset>
        </form>';
    }
};

post '/login' => sub {
    if ( params->{login} eq 'kivu' and params->{pass} eq 'kivu'
    or   params->{login} eq 'test' and params->{pass} eq 'test' ) {
        session loggedin => 1;
        session login    => params->{login};
        redirect '/parties';
    } else {
        redirect '/';
    }
};

any '/logout' => sub {
    if ( session('loggedin') ) {
        session loggedin => 0;
        redirect '/';
    } else {
        redirect '/parties';
    }
};

get '/parties' => sub {
    if ( session('loggedin') ) {
        my $html = "<h1>Party list</h1><table><tr><td>Name</td><td>Map</td><td>Created by</td><td>Join</td></tr>";
        for ( keys %$parties ) {
            my $p = $$parties{$_};
            $html .= "<tr><td>$$p{name}</td><td>$$p{mapname}</td><td>$$p{creator}</td><td><a href=\"/joinparty/$$p{name}\">Join</a></td></tr>";
        }
        $html .= '<table>';
        $html .= '
        <form method="post" action="/ownparty">
            <fieldset>
                <legend>Create a party</legend>
                <p><strong>Name: </strong><input type="text" name="name" /></p>
                <p><strong>Map: </strong>
                    <select name="mapname">
                        <option value="demo">demo</option>
                    </select>
                </p>
                <p><input type="submit" value="Create" /></p>
            </fieldset>
        </form>';
    } else {
        redirect '/';
    }
};

post '/ownparty' => sub {
    if ( session('loggedin') ) {
        my $name = params->{name};

        my $party = {};
        $$party{name}    = $name;
        $$party{mapname} = params->{mapname};
        $$party{map}     = Thetical::Battle::Map::Load( params->{mapname} );
        $$party{chars}   = {};
        $$party{creator} = session->{login};
        $$party{player1} = session->{login};
        
        $$parties{$name} = $party;
        session party => $name;
        session player => 1;
        
        return "
            <h1>$$party{name}</h1>
            <p><strong>Map: $$party{mapname}</strong></p>
            <a href=\"/choosechar\">Start</a>";
    } else {
        redirect '/';
    }
};

get '/joinparty/:name' => sub {
    if ( session('loggedin') ) {
        my $party        = $$parties{params->{name}};
        $$party{player2} = session->{login};
        session party   => params->{name};
        session player  => 2;
        
        return "
            <h1>$$party{name}</h1>
            <p><strong>Map: $$party{mapname}</strong></p>
            <p><strong>Creator: $$party{creator}</strong></p>
            <a href=\"/choosechar\">Start</a>";
    } else {
        redirect '/';
    }
};

get '/choosechar' => sub {
    if ( session('loggedin') ) {
        my $name = session('party');
        my $player = session('player');
        my $party = $$parties{$name};

        if ( $$party{player1} and $$party{player2} ) {
            my @tiles;
            if ( $player == 1 ) {
                @tiles = ( [1,5], [1,6], [1,7], [1,8], [1,9] );
            } elsif ( $player == 2 ) {
                @tiles = ( [19,5], [19,6], [19,7], [19,8], [19,9] );
            }
            
            my $html = '<form method="post" action="/startbattle">';
            $html .= '<p><strong>'.$_->[0].'-'.$_->[1].': </strong><input type="text" name="'.$_->[0].'-'.$_->[1].'"></p>' for @tiles;
            $html .= '<p><input type="submit" value="Battle!" /></p>';
            $html .= '</from>';
            
            return $html;
        } else {
            return 0;
        }
    } else {
        redirect '/';
    }    
};

any '/startbattle' => sub {
     if ( session('loggedin') ) {
     
        my $name = session('party');
        my $player = session('player');
        my $party = $$parties{$name};
        
        if ( $$party{player1started} and $$party{player2started} ) {
            redirect '/client.html';
        } else {
            my %params = params;
            for my $k ( keys %params ) {
                if ( params->{$k} ) {
                    my ($y, $x) = split '-', $k;
                    my $charid  = params->{$k};
                    
                    $$party{map}{tiles}[$y][$x]{char} = $charid;
                    my $char = { 'id'        => $charid
                               , 'hp'        => 10
                               , 'hpmax'     => 10
                               , 'ct'        => 12
                               , 'ctmax'     => 12
                               , 'team'      => $player
                               , 'move'      => 5
                               , 'direction' => 1
                               , 'active'    => 0 };
                    $$party{chars}{$charid} = $char;
                }
            }
            
            if ( $player == 1 ) {
                $$party{player1started} = 1;
            } elsif ( $player == 2 ) {
                $$party{player2started} = 1;
            }
            
            if ( $$party{player1started} and $$party{player2started} ) {
                redirect '/client.html';
            }
        }
    } else {
        redirect '/';
    }     
};

# Decrements all characters CT until a CT hits 0
sub getnextactive {
    my $party = $$parties{session('party')};
    my $chars = $$party{chars};

    for ( keys %$chars ) {
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

# Battle main callback
get '/battle' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};
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
    to_json Thetical::Battle::Move::GetWalkables( $map, $char );
};

# Returns the list of attackables tiles for a character
get '/char/:id/attackables' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};
    my $map   = $$party{map};
    my $char  = $$party{chars}{ params->{id} };
    to_json Thetical::Battle::Attack::GetAttackables( $map, $char );
};

# Move action
get '/char/:id/moveto/:y/:x' => sub {
    return send_error("Not logged in", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not in a started party", 403) unless $$party{player1started} and $$party{player2started};

    my $id = params->{id};
    my $y2 = params->{y};
    my $x2 = params->{x};

    my $map   = $$party{map};
    my $char  = $$party{chars}{ params->{id} };

    # permissions checks
    return send_error("Not this character's turn",             403) unless $$char{active} == 1;
    return send_error("Tile not walkable",                     403) unless Thetical::Battle::Move::IsWalkable( $map, $char, $y2, $x2 );
    return send_error("This character does not belong to you", 403) unless $$char{team} == session->{player};

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

    return to_json $path;
};

# Wait action: this is where charecter's turn ends
get '/char/:id/wait/:direction' => sub {
    return send_error("Not allowed", 403) unless session('loggedin');
    my $party = $$parties{session('party')};
    return send_error("Not allowed", 403) unless $$party{player1started} and $$party{player2started};

    my $id = params->{id};
    
    # permissions checks
    my $char = $$party{chars}{ params->{id} };
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
    
    return send_error("Not allowed", 403) unless $$char1{active} == 1;
    return send_error("Not allowed", 403) unless Thetical::Battle::Attack::IsAttackable( $map, $char1, $char2 );
    return send_error("Not allowed", 403) unless $$char1{team} == session->{player};
    
    $$char2{hp} -= 5;
    $$char2{hp} = 0 if $$char2{hp} < 0;
    
    $$char1{canact} = 0;
    
    return 5;
};

dance;
