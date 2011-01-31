package Thetical::Battle::Move;
use Modern::Perl;
use Thetical::Battle::Character;

# Used in walkable tiles computation and pathfinding
sub _getadjacentwalkables {
    my $map = shift;
    my $w2;

    for my $t1 ( @_ ) {
        my ($y1, $x1) = @$t1;
        for my $tx ( ( [$y1-1, $x1  ]
                     , [$y1+1, $x1  ]
                     , [$y1  , $x1-1]
                     , [$y1  , $x1+1] ) ) {
            eval {
                my ($y2, $x2) = @$tx;
                my $t2 = $$map{tiles}[$y2][$x2];
                if ( $t2 && ! $$t2{char} > 0 ) {
                    push @$w2, [$y2, $x2];
                }
            };
        }
    }

    @$w2;
}

# Compute the list of walkable tiles for a character
sub GetWalkables {
    my ( $map, $char ) = @_;

    my $tile = Thetical::Battle::Character::Coords( $map, $char );
    my @walkables = ( $tile );

    for ( 1..$$char{move} ) {
        push @walkables, _getadjacentwalkables( $map, @walkables );
    }

    # Remove character's tile from the list
    @walkables = map { $_->[0] == $tile->[0] && $_->[1] == $tile->[1] ? () : $_ } @walkables;

    return \@walkables;
}

# Used to check if a tile is walkable for a character
sub IsWalkable {
    my ( $map, $char, $y, $x ) = @_;

    my $walkables = GetWalkables( $map, $char );

    for ( @$walkables ) {
        return 1 if $y == $_->[0] && $x == $_->[1];
    }

    undef;
}

# Returns the character's new direction after a move
# 0 = up, 1 = down, 2 = left, 3 = right
sub GetNewDirection {
    my ( $y1, $x1, $y2, $x2 ) = @_;

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

# Returns the character path from one tile to another
# the path is of the form ['5-5','4-5','4-4']
sub GetPath {
    my ( $map, $char, $y1, $x1, $y2, $x2 ) = @_;

    my $tree = { "$y1-$x1" => {} };
    _buildtree( $map, $tree, $$char{move}-1, "$y2-$x2" );

    my $paths = [];
    _findpathes( $tree, [], $paths );

    return $paths->[0];
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
