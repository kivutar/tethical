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
    
    $map2 = {};
    
    my $height = $$map{y};
    my $width  = $$map{x};
    
    for my $tile ( @{$$map{tiles}} ) {
        $x = $$tile{x};
        $y = $$tile{y};
        $z = $$tile{z};
        $$map2{tiles}[$x][$y][$z] = { walkable => $$tile{walkable} };
    }
    
    return $map2;

#    my $map = {};
#    for my $layer ( qw<heights walkables ground> ) {
#        open FH, "maps/$name.$layer";
#        $$map{$layer} = [ map { chomp $_; [ split /,/ ] } <FH> ];
#        close FH;
#    }

#    my $height = @{$$map{heights}};
#    my $width  = @{$$map{heights}[0]};

#    my $map2 = { name   => $name
#               , height => $height
#               , width  => $width };

#    for my $y (0..$height-1) {
#        for my $x (0..$width-1) {

#            $$map2{tiles}[$y][$x] = { 'height'   => $$map{heights  }[$y][$x]
#                                    , 'walkable' => $$map{walkables}[$y][$x]
#                                    , 'ground'   => $$map{ground   }[$y][$x] };
#        }
#    }

#    $map2;
}

1;
