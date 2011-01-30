package Thetical::Battle::Character;

sub List {
    { '11' => { 'id'        => 11
              , 'hp'        => 10
              , 'hpmax'     => 10
              , 'ct'        => 12
              , 'ctmax'     => 12
              , 'team'      => 1
              , 'move'      => 5
              , 'direction' => 1 }
    , '12' => { 'id'        => 12
              , 'hp'        => 15
              , 'hpmax'     => 15
              , 'ct'        => 10
              , 'ctmax'     => 10
              , 'team'      => 1
              , 'move'      => 4
              , 'direction' => 1 }
    , '13' => { 'id'        => 13
              , 'hp'        => 12
              , 'hpmax'     => 12
              , 'ct'        => 11
              , 'ctmax'     => 11
              , 'team'      => 1
              , 'move'      => 6
              , 'direction' => 1 }
    , '14' => { 'id'        => 14
              , 'hp'        => 13
              , 'hpmax'     => 13
              , 'ct'        => 13
              , 'ctmax'     => 13
              , 'team'      => 1
              , 'move'      => 5
              , 'direction' => 1 }
    , '21' => { 'id'        => 21
              , 'hp'        => 10
              , 'hpmax'     => 10
              , 'ct'        => 12
              , 'ctmax'     => 12
              , 'team'      => 2
              , 'move'      => 5
              , 'direction' => 0 }
    , '22' => { 'id'        => 22
              , 'hp'        => 15
              , 'hpmax'     => 15
              , 'ct'        => 10
              , 'ctmax'     => 10
              , 'team'      => 2
              , 'move'      => 4
              , 'direction' => 0 }
    , '23' => { 'id'        => 23
              , 'hp'        => 12
              , 'hpmax'     => 12
              , 'ct'        => 11
              , 'ctmax'     => 11
              , 'team'      => 2
              , 'move'      => 6
              , 'direction' => 0 }
    , '24' => { 'id'        => 24
              , 'hp'        => 13
              , 'hpmax'     => 13
              , 'ct'        => 13
              , 'ctmax'     => 13
              , 'team'      => 2
              , 'move'      => 5
              , 'direction' => 0 }
    }
};

sub Get {
    my $chars = List();
    return $$chars{shift};
}

# Returns the coordinates of a character
sub getcharcoords {
    my ($id, $map) = @_;

    # loop over all the tiles of the map
    for my $y ( 0..$$map{height}-1 ) {
        for my $x ( 0..$$map{width}-1 ) {

            my $tile = $$map{tiles}[$y][$x];
            
            # return tile coordinates when the character is found
            if ( defined $$tile{char} && $$tile{char} == $id ) {
                return [$y, $x];
            }
        }
    }
}

1;
