
// Draw walkable tiles
function walkables(walkables, id, character) {

    for (var tile in walkables) {
        var i = '#'+walkables[tile][0]+'-'+walkables[tile][1];
        $(i).addClass('walkable');
        if ( character['active'] == 1 ) {
            $(i).addClass('active');
        }
    }

    // Moving
    $('.active.walkable').click(function() {
        var coord = $(this).attr('id').split('-');
        var y = coord[0];
        var x = coord[1];
        if ( confirm('Are you sure you want to move to '+y+','+x+'?') ) {
            $.getJSON('http://localhost:3000/char/'+id+'/moveto/'+y+'/'+x, function(data) {
                $.getJSON('http://localhost:3000/map', map);
            });
        }
    });
}

function get_character(id) {
    var character;
    $.ajax({
        url: 'http://localhost:3000/char/'+id,
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(data) {
            character = data;
        }
    });
    return character;
}

// Build the html map
function map(map) {
    var table = '<table id="map">';
    for (var y in map['tiles']) {
        table += '<tr>';
        for (var x in map['tiles'][y]) {

            var img;
            if ( map['tiles'][y][x]['char'] > 0 ) {
                var id = map['tiles'][y][x]['char'];
                var character = get_character(id);
                img = '<img id="char'+id+'" class="char';
                img += ' team'+character['team'];
                if ( character['active'] == 1 ) {
                    img += ' active';
                }
                img += '" src="images/char.png">';
            } else {
                img = '';
            }

            var height = map['tiles'][y][x]['height'];
            var ground = map['tiles'][y][x]['ground'];
            
            table += '<td id="'+y+'-'+x+'"';
            table += ' class="';
            table += ' height'+height;
            table += ' ground'+ground;
            table += '">';
            table += img;
            table += '</td>';
        }
        table += '</tr>';
    }
    table += '</table>';
    $('body').html(table);
    
    // Clicking on a character
    $('.char').click(function() {
        var id = $(this).attr('id').replace('char','');
        $.getJSON('http://localhost:3000/char/'+id+'/walkables', function(data) { walkables(data, id, get_character(id)); } );
    });
    
    // Remove walkable overlay on focus out
    $("td[class!='walkable']").click(function() { $('td').removeClass('walkable').removeClass('active'); });
}

// Starting point
$(document).ready(function() {
    $.getJSON('http://localhost:3000/map', map);
});

