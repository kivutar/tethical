package Tethical::Battle::Map;
use JSON;
use Data::Dumper qw<Dumper>;

# Open the map files, and return the map data structure
sub Load {
    my $name = shift;
    
    local $/;
    open FH, "maps/$name.json";
    $map = decode_json <FH>;
    close FH;
    
    for my $tile ( @{$$map{tiles}} ) {
        $x = $$tile{x};
        $y = $$tile{y};
        $z = $$tile{z};
        $$map{tiles2}[$x][$y][$z] = $tile;
    }
    
    $$map{tiles} = $$map{tiles2};
    $$map{tiles2} = undef;
    
    return $map;
}

1;
