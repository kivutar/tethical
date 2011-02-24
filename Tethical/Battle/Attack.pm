package Tethical::Battle::Attack;
use Modern::Perl;
use Tethical::Battle::Character;

# Compute the list of attackable tiles for a character
sub GetAttackables {
    my ( $map, $char ) = @_;

    my $t1 = Tethical::Battle::Character::Coords( $map, $char );
    my ($y1, $x1) = @$t1;
    
    my $a;
    for my $tx ( ( [$y1-1, $x1  ]
                 , [$y1+1, $x1  ]
                 , [$y1  , $x1-1]
                 , [$y1  , $x1+1] ) ) {
        eval {
            my ($y2, $x2) = @$tx;
            my $t2 = $$map{tiles}[$y2][$x2];
            if ( $t2 && ! $$t2{walkables} == 1 ) {
                push @$a, [$y2, $x2];
            }
        };
    }

    return $a;
}

# Used to check if a tile is walkable for a character
sub IsAttackable {
    my ( $map, $char1, $char2 ) = @_;

    my $attackables = GetAttackables( $map, $char1 );

    my $tile2 = Tethical::Battle::Character::Coords( $map, $char2 );
    my $y2 = $tile2->[0];
    my $x2 = $tile2->[1];

    for ( @$attackables ) {
        return 1 if $y2 == $_->[0] && $x2 == $_->[1];
    }

    undef;
}

1;
