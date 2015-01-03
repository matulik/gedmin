var load = "<img src=/static/img/loading.gif>";
var deamonsinterval = setInterval("deamons();", 1000);

function stopdeamons() {
    clearInterval(deamonsinterval);
}

function infoWindow(deamon) {

}

function formgen(service, status) {
    var retHTML = '';
    retHTML += '\n<div class="dname_' + service + '">usługa: ' + service + '</div>';
    retHTML += '\n<div class="dstat">status: ' + status + '</div>';
    retHTML += '\n<div class="dbuts">';

    retHTML += '\n<form id="' + service + '_start" action="/inits/startD/" method="post" target="_blank">';
    retHTML += '\n<input type="hidden" name="deamon" value="' + service + '">';
    retHTML += '\n<input type="submit" value="Start" class="btn btn-default" style="width: 100px; height: 30px">';
    retHTML += '\n</form>';

    retHTML += '\n<form id="' + service + '_stop" action="/inits/stopD/" method="post" target="_blank">';
    retHTML += '\n<input type="hidden" name="deamon" value="' + service + '">';
    retHTML += '\n<input type="submit" value="Stop" class="btn btn-default" style="width: 100px; height: 30px">';
    retHTML += '\n</form>';

    retHTML += '\n<form id="' + service + '_restart" action="/inits/restartD/" method="post" target="_blank">';
    retHTML += '\n<input type="hidden" name="deamon" value="' + service + '">';
    retHTML += '\n<input type="submit" value="Restart" class="btn btn-default" style="width: 100px; height: 30px">';
    retHTML += '\n</form>';

    return retHTML;
}


function prepareDList(list) {
    d = [];
    n = 0;
    for (var i = 0; i < list.length; i++) {
        if (list[i] == " ") {
            d[d.length] = list.slice(n, i);
            n = i;
        }
        if (list[i] == "\n") {
            n = i + 1;
        }
    }
    return d
}

function prepareSList(list) {
    s = [];
    n = 0;
    for (var i = 0; i < list.length; i++) {
        if (list[i] == " ") {
            n = i;
        }
        if (list[i] == "\n") {
            s[s.length] = list.slice(n, i);
            n = i;
        }
    }
    return s
}

function deamons() {
    $.ajax({
        type: 'POST',
        url: '/inits_aj/deamons/',
        success: function (j) {
            if (j == "") {
                $('#deamons').html(load);
            }
            else {
                //$('#deamons').html(j);
                d = prepareDList(j);
                s = prepareSList(j);
                form = "";
                for (var i = 0; i < d.length; i++) {
                    form += formgen(d[i], s[i]);
                }

                $('#deamons').html(form);
            }
        }
    });
}