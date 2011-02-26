
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
        var table = '<div id="map"><table>';
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
        table += '<p><button id="refresh">Refresh</button></p>';
        table += '</div>';
        $('body').html(table);
        
        $('button#refresh').click(function() {
            $.ajax({
                url: 'http://localhost:3000/battle',
                type: 'get',
                dataType: 'json',
                async: false,
                success: battle,
            });
        });
        
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

function refresh_battle_begins() {
    $.ajax({
        url: 'http://localhost:3000/party',
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(party) {
            if ( party['player1started'] && party['player2started'] ) {
                $.ajax({
                    url: 'http://localhost:3000/battle',
                    type: 'get',
                    dataType: 'json',
                    async: false,
                    success: battle,
                });
            }
        }
    });
}

function battle_begins() {
    var html  = '<h1>Waiting for the other player</h1>';
        html += '<p><button id="refresh">Refresh</button></p>';
    $('body').html(html);
    
    refresh_battle_begins();
    $('button#refresh').click( refresh_battle_begins );
}

function characters_selected(e) {
    e.preventDefault();
    
    var data = {};
    $('input[type="text"]').each(function() {
        data[$(this).attr('name')] = $(this).val();
    });
    
    $.ajax({
        url: 'http://localhost:3000/startbattle',
        type: 'post',
        dataType: 'json',
        async: false,
        data: data,
        success: battle_begins,
    });
}

function character_selection() {
     $.ajax({
        url: 'http://localhost:3000/choosechar',
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(tiles) {
            var html  = '<h1>Character selection</h1>';
                html += '<form method="post">';
                html += '   <fieldset>';
                for ( k in tiles ) {
                    html += '   <p><strong>'+tiles[k][0]+'-'+tiles[k][1]+'-'+tiles[k][2]+': </strong><input type="text" name="'+tiles[k][0]+'-'+tiles[k][1]+'"></p>';
                }
                html += '       <p><input type="submit" value="Battle!" /></p>'
                html += '   </fieldset>';
                html += '</form>';
            $('body').html(html);
            
            $('input[type="submit"]').click( characters_selected );
        },
    });   
}

function refresh_party() {
    $.ajax({
        url: 'http://localhost:3000/party',
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(party) {
            var html = '';
            if ( party['player2'] ) {
                html += '<p><strong>Player2: </strong>'+party['player2']+'</p>';
                html += '<p><button id="start">Start character selection</button></p>';
            } else {
                html += '<p>Waiting for player2...</p>';
            }
            $('div').html(html);
            $('button#start').click( character_selection );
        },
    });
}

function party(party) {
    var html  = '<h1>Party: '+party['name']+'</h1>';
        html += '<p><strong>Created by: </strong>'+party['creator']+'</p>';
        html += '<p><strong>Map: </strong>'+party['mapname']+'</p>';
        html += '<p><strong>Player1: </strong>'+party['player1']+'</p>';
        html += '<div></div>';
        html += '<p><button id="refresh">Refresh</button></p>';
    $('body').html(html);
    
    refresh_party();
    $('button#refresh').click( refresh_party );
}

function ownparty(e) {
    e.preventDefault();

    var name    = $('input[name="name"    ]').val();
    var mapname = $('select[name="mapname"]').val();

    $.ajax({
        url: 'http://localhost:3000/ownparty',
        type: 'post',
        dataType: 'json',
        async: false,
        data: { name: name, mapname: mapname },
        success: party,
    });
}

function joinparty() {
    var name = $(this).attr('id');
    $.ajax({
        url: 'http://localhost:3000/joinparty/'+name,
        type: 'post',
        dataType: 'json',
        async: false,
        success: party,
    });
}

function refresh_parties() {
    $('tbody').empty();
    $.ajax({
        url: 'http://localhost:3000/parties',
        type: 'get',
        dataType: 'json',
        async: false,
        success: function(parties) {
            for ( key in parties ) {
                $('tbody').append('<tr><td>'+key+'</td><td>'+parties[key]['mapname']+'</td><td>'+parties[key]['creator']+'</td><td><button class="join" id="'+key+'">Join</button></td></tr>');
            }
        },
    });
    $('button.join').click( joinparty );
    //setTimeout(refresh_parties, 1000);
}

function parties() {
    var html  = '<h1>Party list</h1>';
        html += '<table>';
        html += '<thead><tr><td>Name</td><td>Map</td><td>Created by</td><td>Join</td></tr></thead>';
        html += '<tbody></tbody>';
        html += '</table>';
        html += '<p><button id="refresh">Refresh</button></p>';
        html += '<form method="post">';
        html += '    <fieldset>';
        html += '        <legend>Create a party</legend>';
        html += '        <p><strong>Name: </strong><input type="text" name="name" /></p>';
        html += '        <p><strong>Map: </strong>';
        html += '            <select name="mapname">';
        html += '                <option value="demo">demo</option>';
        html += '                <option value="Test City">Test City</option>';
        html += '            </select>';
        html += '        </p>';
        html += '        <p><input type="submit" value="Create" /></p>';
        html += '    </fieldset>';
        html += '</form>';
    $('body').html(html);
    
    $('input[type="submit"]').click( ownparty );
    $('button#refresh').click( refresh_parties );
}

function login(e) {
    e.preventDefault();

    var login = $('input[name="login"]').val();
    var pass  = $('input[name="pass" ]').val();
    
    $.ajax({
        url: 'http://localhost:3000/login',
        type: 'post',
        dataType: 'json',
        async: false,
        data: { login: login, pass: pass },
        success: parties,
    });
}

// Starting point
$(document).ready(function() {
    var html  = '<h1>Tethical</h1>';
        html += '<form method="post">';
        html += '   <fieldset>';
        html += '       <legend>Login</legend>';
        html += '       <p><strong>Login: </strong><input type="text" name="login" /></p>';
        html += '       <p><strong>Pass: </strong><input type="password" name="pass" /></p>';
        html += '       <p><input type="submit" value="Login" /></p>';
        html += '   </fieldset>';
        html += '</form>';
    $('body').html(html);
    
    $('input[type="submit"]').click( login );
});

