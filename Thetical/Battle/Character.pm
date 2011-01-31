package Thetical::Battle::Character;
use Modern::Perl;

# Returns the coordinates of a character
sub Coords {
    my ( $map, $char ) = @_;

    # loop over all the tiles of the map
    for my $y ( 0..$$map{height}-1 ) {
        for my $x ( 0..$$map{width}-1 ) {

            my $tile = $$map{tiles}[$y][$x];
            
            # return tile coordinates when the character is found
            if ( defined $$tile{char} && $$tile{char} == $$char{id} ) {
                return [$y, $x];
            }
        }
    }
}

1;
