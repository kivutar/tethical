function walkables(walkables) {
    for (var tile in walkables) {
        $('#'+walkables[tile][0]+'-'+walkables[tile][1]).addClass('walkable');
    }
}

function map(map) {
    var table = '<table id="map">';
    for (var y in map['tiles']) {
        table += '<tr>';
        for (var x in map['tiles'][y]) {
            var character = map['tiles'][y][x]['char'] > 0 ? '<img id="char'+map['tiles'][y][x]['char']+'" class="char" src="images/char.png">' : '';
            var height = map['tiles'][y][x]['height'];
            var ground = map['tiles'][y][x]['ground'];
            
            table += '<td id="'+y+'-'+x+'"';
            table += ' class="';
            table += ' height'+height;
            table += ' ground'+ground;
            table += '">';
            table += character;
            table += '</td>';
        }
        table += '</tr>';
    }
    table += '</table>';
    $('body').html(table);
    
    $('.char').click(function() {
        var id = $(this).attr('id').replace('char','');
        $.get('http://localhost:3000/char/'+id+'/walkables', walkables, 'json');
    });
    
    $("td").click(function() { $('td').removeClass('walkable'); });
}

$(document).ready(function() {
    $.get('http://localhost:3000/map',map,'json');
});

