package Tethical::Battle::Attack;
use Modern::Perl;
use Tethical::Battle::Character;

# Compute the list of attackable tiles for a character
sub GetAttackables {
    my ( $map, $char ) = @_;

    my $t1 = Tethical::Battle::Character::Coords( $map, $char );
    my ($x1, $y1, $z1) = @$t1;
    
    my $a;
    for my $tx ( ( [$x1-1, $y1  ]
                 , [$x1+1, $y1  ]
                 , [$x1  , $y1-1]
                 , [$x1  , $y1+1] ) ) {
        eval {
            my ($x2, $y2) = @$tx;
            my $t2 = $$map{tiles}[$x2][$y2];
            
            if ( $t2 && $x2 >= 0 && $y2 >= 0 ) {
                for (my $z2=0; $z2 < @$t2; $z2++ ) {
                    my $t3 = $$map{tiles}[$x2][$y2][$z2];
                    if ( $t3 && $$t3{walkable} && $$t3{selectable} && abs($z2-$z1) <= 4 ) {
                        push @$a, [$x2, $y2, $z2];
                    }
                }
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
    my $x2 = $tile2->[0];
    my $y2 = $tile2->[1];
    my $z2 = $tile2->[2];

    for ( @$attackables ) {
        return 1 if $x2 == $_->[0] && $y2 == $_->[1] && $z2 == $_->[2];
    }

    undef;
}

1;
