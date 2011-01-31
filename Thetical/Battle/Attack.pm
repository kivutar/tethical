package Thetical::Battle::Attack;
use Modern::Perl;
use Thetical::Battle::Character;

# Compute the list of attackable tiles for a character
sub GetAttackables {
    my ( $map, $char ) = @_;

    my $t1 = Thetical::Battle::Character::Coords( $map, $char );
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
    my ( $map, $char, $y, $x ) = @_;

    my $attackables = GetAttackables( $map, $char );

    for ( @$attackables ) {
        return 1 if $y == $_->[0] && $x == $_->[1];
    }

    undef;
}

1;
