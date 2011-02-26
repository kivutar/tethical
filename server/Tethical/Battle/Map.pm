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
    
    $map2 = { chartiles => $$map{chartiles} };
    
    my $height = $$map{y};
    my $width  = $$map{x};
    
    for my $tile ( @{$$map{tiles}} ) {
        $x = $$tile{x};
        $y = $$tile{y};
        $z = $$tile{z};
        $$map2{tiles}[$x][$y][$z] = { walkable => $$tile{walkable} };
    }
    
    return $map2;
}

1;
