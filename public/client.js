
// Draw walkable tiles
function display_walkables(walkables, character) {

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
            $.getJSON('http://localhost:3000/char/'+character['id']+'/moveto/'+y+'/'+x, function(data) {
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
    var table = '<table>';
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
                var direction = character['direction'];
                img += '" src="images/char'+direction+'.png">';
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
    $('#map').html(table);
    
    // Clicking on a character
    $('.char').click(function() {
        var id = $(this).attr('id').replace('char','');
        var character = get_character(id);
        display_status(character);
        if ( character['active'] == 1 ) {
            display_active_menu(character);
        } else {
            display_passive_menu(character);
        }
    });
    
    // Remove walkable overlay on focus out
    $("td[class!='walkable']").click(function() {
        $('td').removeClass('walkable').removeClass('active');
    });
    
    $('#menu').empty();
}

function display_status(character) {
    var status = '<table>';
    status += '<tr><th>HP</th><td>'+character['hp']+'/'+character['hpmax']+'</td></tr>';
    status += '<tr><th>CT</th><td>'+character['ct']+'/'+character['ctmax']+'</td></tr>';
    status += '</table>';
    $('#character').html(status);
}

function display_passive_menu(character) {
    var menu = '<ul>';
    menu += '<li id="btnMove">Show Move</li>';
    menu += '<li id="btnStatus">Status</li>';
    menu += '</ul>';
    $('#menu').html(menu);
    
    $('#btnMove').click(function() {
        $.getJSON('http://localhost:3000/char/'+character['id']+'/walkables', function(data) { display_walkables(data, character); } );
    });
}

function display_active_menu(character) {
    var menu = '<ul>';
    var canmove = character['canmove'] == 1 ? 'enabled' : 'disabled';
    menu += '<li id="btnMove" class="'+canmove+'">Move</li>';
    menu += '<li id="btnAct">Action</li>';
    menu += '<li id="btnStatus">Status</li>';
    menu += '<li id="btnWait">Wait</li>';
    menu += '</ul>';
    $('#menu').html(menu);
    
    $('#btnMove').click(function() {
        $.getJSON('http://localhost:3000/char/'+character['id']+'/walkables', function(data) { display_walkables(data, character); } );
    });
    
    /*$('#btnAct').click(function() {
        $.getJSON('http://localhost:3000/char/'+character['id']+'/walkables', function(data) { display_walkables(data, character); } );
    });*/
    
    $('#btnWait').click(function() {
        $.getJSON(
            'http://localhost:3000/char/'+character['id']+'/wait/'+character['direction'], 
            function(data) { $.getJSON('http://localhost:3000/map', map);
        } );
    });
}

// Starting point
$(document).ready(function() {
    $.getJSON('http://localhost:3000/map', map);
});

