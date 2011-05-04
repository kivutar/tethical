package Tethical::Battle::Move;
use Modern::Perl;
use Tethical::Battle::Character;

# Used in walkable tiles computation and pathfinding
sub _getadjacentwalkables {
    my $map = shift;
    my @w2;

    for my $t1 ( @_ ) {
        my ($x1, $y1, $z1) = @$t1;
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
                        if ( $t3 && ! $$t3{char} > 0 && $$t3{walkable} && $$t3{selectable} ) {
                            push @w2, [$x2, $y2, $z2];
                        }
                    }
                }
            };
        }
    }

    @w2;
}

# Compute the list of walkable tiles for a character
sub GetWalkables {
    my ( $map, $char ) = @_;

    my $tile = Tethical::Battle::Character::Coords( $map, $char );
    my @walkables = ( $tile );

    for ( 1..$$char{move} ) {
        push @walkables, _getadjacentwalkables( $map, @walkables );
    }

    # Remove character's tile from the list
    @walkables = map { $_->[0] == $tile->[0] && $_->[1] == $tile->[1] && $_->[2] == $tile->[2] ? () : $_ } @walkables;

    return \@walkables;
}

# Used to check if a tile is walkable for a character
sub IsWalkable {
    my ( $map, $char, $x, $y, $z ) = @_;

    my $walkables = GetWalkables( $map, $char );

    for ( @$walkables ) {
        return 1 if $x == $_->[0] && $y == $_->[1] && $z == $_->[2];
    }

    undef;
}

# Returns the character's new direction after a move
# 0 = up, 1 = down, 2 = left, 3 = right
sub GetNewDirection {
    my ( $x1, $y1, $x2, $y2 ) = @_;

    # compute the move vector
    my $dx = $x2 - $x1;
    my $dy = $y2 - $y1;
    
    # was the move more hortizontal of vertical ?
    if ( $dy*$dy > $dx*$dx ) {
        return $dy > 0 ? 1 : 0; # up or down ?
    } else {
        return $dx > 0 ? 2 : 3; # left or right ?
    }
}

# Returns the character path from one tile to another
# the path is of the form ['5-5-2','4-5-2','4-4-2']
sub GetPath {
    my ( $map, $char, $x1, $y1, $z1, $x2, $y2, $z2 ) = @_;

    my $tree = { "$x1-$y1-$z1" => {} };
    _buildtree( $map, $tree, $$char{move}-1, "$x2-$y2-$z2" );

    my $paths = [];
    _findpathes( $tree, [], $paths );

    return [ map { [ map { int($_) } split '-', $_ ] } @{ $paths->[0] } ];
}

# Recursively builds the paths tree
sub _buildtree {
    my ( $map, $tree, $moves, $dest ) = @_;
    
    for my $k1 ( keys %$tree ) {
        
        for ( _getadjacentwalkables( $map, [ split '-', $k1 ] ) ) {
            my $k2 = join '-', @$_;

            if ( $k2 eq $dest ) {
                $$tree{$k1}{$k2} = 'X'; return;
            } else {
                $$tree{$k1}{$k2} = {};
            }
        }
        
        _buildtree( $map, $$tree{$k1}, $moves-1, $dest ) if $moves > 0;
    }
}

# Recursively browse the paths tree to extract the pathes
sub _findpathes {
    my ( $tree, $p, $paths ) = @_;

    for ( keys %$tree ) {
        if ( $$tree{$_} eq 'X' ) {
            push @$paths, [ @$p, ( $_ ) ];
        } else {
            _findpathes( $$tree{$_}, [ @$p, ( $_ ) ], $paths );
        }
    }
}

1;
