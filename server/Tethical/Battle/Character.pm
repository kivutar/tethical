package Tethical::Battle::Character;
use Modern::Perl;

# Returns the coordinates of a character
sub Coords {
    my ( $map, $char ) = @_;

    # loop over all the tiles of the map
    for my $x ( 0..$$map{x}-1 ) {
        for my $y ( 0..$$map{y}-1 ) {
            for my $z ( 0..$$map{z}-1 ) {

                my $tile = $$map{tiles}[$x][$y][$z];
                
                # return tile coordinates when the character is found
                if ( defined $$tile{char} && $$tile{char} == $$char{id} ) {
                    return [$x, $y, $z];
                }
            }
        }
    }
}

1;
