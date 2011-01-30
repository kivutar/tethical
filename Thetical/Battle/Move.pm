package Thetical::Battle::Move;
use Thetical::Battle::Character;
use Data::Dumper qw<Dumper>;

# Used in walkable tiles computation and pathfinding
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

# Compute the list of walkable tiles for a character
sub getwalkables {
    my ( $id, $map ) = @_;
    my $char = Thetical::Battle::Character::Get( $id );
    warn Dumper $char;
    my $tile = Thetical::Battle::Character::getcharcoords( $id, $map );
    my @walkables = ( $tile );

    for ( 1..$$char{move} ) {
        push @walkables, getadjacentwalkables( @walkables );
    }

    # Remove character's tile from the list
    @walkables = map { $_->[0] == $tile->[0] && $_->[1] == $tile->[1] ? () : $_ } @walkables;

    return \@walkables;
}

# Used to check if a tile is walkable for a character
sub is_walkable {
    my ($id, $y, $x) = @_;

    my $walkables = getwalkables($id);

    for ( @$walkables ) {
        return 1 if $y == $_->[0] && $x == $_->[1];
    }

    undef;
}

# Returns the character's new direction after a move
# 0 = up, 1 = down, 2 = left, 3 = right
sub getnewdirection {
    my ($y1, $x1, $y2, $x2) = @_;

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
sub getpath {
    my ($id, $y1, $x1, $y2, $x2) = @_;
    
    my $tree = { "$y1-$x1" => {} };
    buildtree( $tree, $$chars{$id}{move}-1, "$y2-$x2" );

    my $paths = [];
    findpathes( $tree, [], $paths );
    return $paths->[1];
}

# Recursively builds the paths tree
sub buildtree {
    my ( $tree, $moves, $dest ) = @_;
    
    for my $k1 ( keys %$tree ) {
        
        for ( getadjacentwalkables( [ split '-', $k1 ] ) ) {
            my $k2 = join '-', @$_;

            if ( $k2 eq $dest ) {
                $$tree{$k1}{$k2} = 'X'; return;
            } else {
                $$tree{$k1}{$k2} = {};
            }
        }
        
        buildtree( $$tree{$k1}, $moves-1, $dest ) if $moves > 0;
    }
}

# Recursively browse the paths tree to extract the pathes
sub findpathes {
    my ( $tree, $p, $paths ) = @_;

    for ( keys %$tree ) {
        if ( $$tree{$_} eq 'X' ) {
            push @$paths, [ @$p, ( $_ ) ];
        } else {
            findpathes( $$tree{$_}, [ @$p, ( $_ ) ], $paths );
        }
    }
}

1;
