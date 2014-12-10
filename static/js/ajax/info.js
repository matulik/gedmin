var load = "<img src=/static/img/loading.gif>";
var servertimeinterval = setInterval("servertime();", 1000);
var systeminterval = setInterval("system();", 1000);
var drivesinterval = setInterval("drives();", 1000);
var networkinterval = setInterval("network();", 1000);

function stopservertime() {
    clearInterval(servertimeinterval);
}

function stopdrives() {
    clearInterval(drivesinterval);
}

function stopnetwork() {
    clearInterval(networkinterval);
}

function stopsystem() {
    clearInterval(systeminterval);
}

function servertime() {
    stopdrives();
    stopnetwork();
    stopsystem();
    $.ajax({
        type: 'POST',
        url: '/info_aj/servertime/',
        success: function (j) {
            //j = j.replace(/\n/g,"<br>")
            if (j == "") {
                $('#time').html(load);
            }
            else {
                $('#time').html(j);
            }
        }
    });
}

function system() {
    stopservertime();
    stopdrives();
    stopnetwork();
    var serverdate = false;
    var kernelinfo = false;
    var uptime = false;
    $.ajax({
        type: 'POST',
        url: '/info_aj/serverdate/',
        async: false,
        success: function (j) {
            //j = j.replace(/\n/g,"<br>")
            if (j == "running") {
                $('#serverdate').html(load);
            }
            else {
                serverdate = true;
                $('#serverdate').html(j);
            }
        }
    });

    $.ajax({
        type: 'POST',
        url: '/info_aj/kernelinfo/',
        async: false,
        success: function (j) {
            //j = j.replace(/\n/g,"<br>")
            if (j == "running") {
                $('#kernelinfo').html(load);
            }
            else {
                kernelinfo = true;
                $('#kernelinfo').html(j);
            }
        }
    });

    $.ajax({
        type: 'POST',
        url: '/info_aj/uptime/',
        async: false,
        success: function (j) {
            //j = j.replace(/\n/g,"<br>")
            if (j == "running") {
                $('#uptime').html(load);
            }
            else {
                uptime = true;
                $('#uptime').html(j);
            }
        }
    });
    if (serverdate == true && kernelinfo == true && uptime == true) {
        stopsystem();
    }
}

function drives() {
    stopservertime();
    stopsystem();
    stopnetwork();
    var hddlist = false;
    var partlist = false;
    var hddtemp = false;
    $.ajax({
        type: 'POST',
        url: '/info_aj/hddlist/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>")
            if (j == "running") {
                $('#hddlist').html(load);
            }
            else {
                hddlist = true;
                $('#hddlist').html(j);
            }
        }
    });

    $.ajax({
        type: 'POST',
        url: '/info_aj/partlist/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>")
            if (j == "running") {
                $('#partlist').html(load);
            }
            else {
                partlist = true;
                $('#partlist').html(j);
            }
        }
    });

    $.ajax({
        type: 'POST',
        url: '/info_aj/hddtemp/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>")
            if (j == "running") {
                $('#hddtemp').html(load);
            }
            else {
                hddtemp = true;
                $('#hddtemp').html(j);
                stopdrives();
            }
        }
    });

    if (hddlist == true && partlist == true && hddtemp == true) {
        stopnetwork();
    }

}

function network() {
    stopservertime();
    stopsystem();
    stopdrives();
    var netdevs = false;
    var globalip = false;
    var localip = false;
    var pinginfo = false;
    $.ajax({
        type: 'POST',
        url: '/info_aj/netdevs/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>")
            if (j == "running") {
                $('#netdevs').html(load);
            }
            else {
                $('#netdevs').html(j);
                netdevs = true;
            }
        }
    });

    $.ajax({
        type: 'POST',
        url: '/info_aj/localip/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>")
            if (j == "running") {
                $('#localip').html(load);
            }
            else {
                $('#localip').html(j);
                localip = true;
            }
        }
    });

    $.ajax({
        type: 'POST',
        url: '/info_aj/globalip/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>")
            if (j == "running") {
                $('#globalip').html(load);
            }
            else {
                $('#globalip').html(j);
                globalip = true;
            }
        }
    });

    $.ajax({
        type: 'POST',
        url: '/info_aj/pinginfo/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>")
            if (j == "running") {
                $('#pinginfo').html(load);
            }
            else {
                pinginfo = true;
                $('#pinginfo').html(j);
            }
        }
    });

    if (pinginfo == true && globalip == true && localip == true && netdevs == true) {
        stopnetwork();
    }

}