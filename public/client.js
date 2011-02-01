
// Draw walkable tiles
function display_walkables(walkables, id) {

    var active = is_active(id);

    for (var tile in walkables) {
        var i = '#'+walkables[tile][0]+'-'+walkables[tile][1];
        $(i).addClass('walkable');
        if ( active ) {
            $(i).addClass('active');
        }
    }

    // Moving
    $('.active.walkable').click(function(e) {
        var coord = $(this).attr('id').split('-');
        var y = coord[0];
        var x = coord[1];
        if ( confirm('Are you sure you want to move to '+y+','+x+'?') ) {
            $.getJSON('http://localhost:3000/char/'+id+'/moveto/'+y+'/'+x, function(data) {
                $.ajax({
                    url: 'http://localhost:3000/battle',
                    type: 'get',
                    dataType: 'json',
                    async: false,
                    success: battle
                });
                display_menu(id, e);
            });
        }
    });
}

// Draw attackables tiles
function display_attackables(attackables, id1) {

    for (var tile in attackables) {
        var i = '#'+attackables[tile][0]+'-'+attackables[tile][1];
        $(i).addClass('attackable');
    }

    // Attacking
    $('.attackable>.char').click(function(e) {
        var id2 = $(this).attr('id').replace('char','');

        if ( confirm('Are you sure you want to attack '+id2+'?') ) {
            $.getJSON('http://localhost:3000/char/'+id1+'/attack/'+id2, function(data) {
                $.ajax({
                    url: 'http://localhost:3000/battle',
                    type: 'get',
                    dataType: 'json',
                    async: false,
                    success: battle
                });
                alert('Infliged '+data+' damages.');
                display_menu(id1, e);
            });
        }
    });
}

function is_active(id) {
    var character = get_character(id);
    return character['active'] == 1;
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

// Battle main callback
function battle(party) {
    if ( 0 ) { //! party['yourturn'] ) {
        alert('Wait. Not your turn');
    } else {
        var map = party['map'];
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
                    if ( character['hp'] > 0 ) {
                        if ( character['active'] == 1 ) {
                            img += ' active';
                        }
                        var direction = character['direction'];
                        img += '" src="images/char'+direction+'.png">';
                    } else {
                        img += '" src="images/char_dead.png">';
                    }
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
        $('.char').click(function(e) {
            var id = $(this).attr('id').replace('char','');
            
            if ( ! $(this).parent().hasClass('attackable') ) {
                display_menu(id, e);
            }
        });
        
        // Remove walkable overlay on focus out
        $("td").click(function() {
            $('td').removeClass('walkable')
                   .removeClass('active')
                   .removeClass('attackable');
        });
    }
}

function modal(content, e) {
    var modal = $('<div id="modal"><div class="overlay"></div><div class="menu">'+content+'<ul></div></div>');
    $('body').append(modal);
    if ( e ) {
        $('#modal>.menu').css('top' , e.pageY);
        $('#modal>.menu').css('left', e.pageX);
    }
    $('.overlay').click(function() {
        modal.remove();
    });
    return modal;
}

function display_status(id) {
    var character = get_character(id);
    var status = '<table>';
    status += '<tr><th>HP</th><td>'+character['hp']+'/'+character['hpmax']+'</td></tr>';
    status += '<tr><th>CT</th><td>'+character['ct']+'/'+character['ctmax']+'</td></tr>';
    status += '</table>';
    modal(status);
}

function display_menu(id, e) {
    var character = get_character(id);

    var menu = '<ul>';

    if ( character['active'] == 1 ) {
        var canmove = character['canmove'] == 1 ? 'enabled' : 'disabled';
        menu += '<li id="btnMove" class="'+canmove+'">Move</li>';
        var canact = character['canact'] == 1 ? 'enabled' : 'disabled';
        menu += '<li class="'+canact+'">Action<ul class="menu"><li id="btnAttack">Attack</li></ul></li>';
    } else {
        menu += '<li id="btnMove">Show Move</li>';
    }

    menu += '<li id="btnStatus">Status</li>';

    if ( character['active'] == 1 ) {
        menu += '<li id="btnWait">Wait</li>';
    }
    menu += '</ul>';
    var mdl = modal(menu, e);

    $('#btnMove').click(function() {
        $.getJSON('http://localhost:3000/char/'+id+'/walkables', function(data) { mdl.remove(); display_walkables(data, id); } );
    });

    $('#btnAttack').click(function() {
        $.getJSON('http://localhost:3000/char/'+id+'/attackables', function(data) { mdl.remove(); display_attackables(data, id); } );
    });

    $('#btnStatus').click(function() {
        $.getJSON('http://localhost:3000/char/'+id+'/walkables', function(data) { display_status(id); } );
    });

    $('#btnWait').click(function() {
        $.getJSON(
            'http://localhost:3000/char/'+id+'/wait/'+character['direction'], 
            function(data) { mdl.remove(); $.getJSON('http://localhost:3000/battle', battle);
        } );
    });
}

// Starting point
$(document).ready(function() {
    $.getJSON('http://localhost:3000/battle', battle);
});

