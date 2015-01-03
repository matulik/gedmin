var interval = setInterval("runwindow();", 500);

function runwindow() {
    $.ajax({
        type: 'POST',
        url: '/inits_aj/deamonoutput/',
        success: function (j) {
            $('#info').html(j);
        }

    });
}

function closewindow() {
    close();
}