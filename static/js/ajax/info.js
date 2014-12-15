var load = "<img src=/static/img/loading.gif>";
var servertimeinterval = setInterval("servertime();", 200);
var systeminterval = setInterval("system();", 1000);
var drivesinterval = setInterval("drives();", 1000);
var networkinterval = setInterval("network();", 1000);
var cpuinterval = setInterval("cpu();", 1000);
var meminterval = setInterval("mem();", 500);


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

function stopcpu() {
    clearInterval(cpuinterval);
}

function stopmem() {
    clearInterval(meminterval);
}

function barret(p) {
    if (p >= 0 && p <= 5)
        return 1;
    else if (p > 5 && p <= 10)
        return 2;
    else if (p > 10 && p <= 15)
        return 3;
    else if (p > 15 && p <= 20)
        return 4;
    else if (p > 20 && p <= 25)
        return 5;
    else if (p > 25 && p <= 30)
        return 6;
    else if (p > 30 && p <= 35)
        return 7;
    else if (p > 35 && p <= 40)
        return 8;
    else if (p > 40 && p <= 45)
        return 9;
    else if (p > 45 && p <= 50)
        return 10;
    else if (p > 50 && p <= 55)
        return 11;
    else if (p > 55 && p <= 60)
        return 12;
    else if (p > 60 && p <= 65)
        return 13;
    else if (p > 65 && p <= 70)
        return 14;
    else if (p > 70 && p <= 75)
        return 15;
    else if (p > 75 && p <= 80)
        return 16;
    else if (p > 80 && p <= 85)
        return 17;
    else if (p > 85 && p <= 90)
        return 18;
    else if (p > 90 && p <= 95)
        return 19;
    else if (p > 95 && p <= 100)
        return 20;
}

function stringFill(n, c) {
    var s = "";
    while (s.length < n) s += c;
    return s;
}

function membar_ph(total, free, buff, cache) {
    var data = total - free - buff - cache;
    data_p = (data / total).toPrecision(3) * 100;
    free_p = (free / total).toPrecision(3) * 100;
    buff_p = (buff / total).toPrecision(3) * 100;
    cache_p = (cache / total).toPrecision(3) * 100;
    retbar = "[ " + stringFill(barret(free_p), "-") + stringFill(barret(buff_p), "~") + stringFill(barret(cache_p), "/") + stringFill(barret(data_p), "|") + " ]";
    return retbar;
}

function membar_sw(total, free) {
    var data = total - free;
    data_p = (data / total).toPrecision(3) * 100;
    free_p = (free / total).toPrecision(3) * 100;
    retbar = "[ " + stringFill(barret(free_p), "-") + stringFill(barret(data_p), "|") + " ]";
    return retbar
}

function servertime() {
    //STOPING ANOTHER INTERCALS
    stopdrives();
    stopnetwork();
    stopsystem();
    stopcpu();
    stopmem();
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
    //STOPING ANOTHER INTERCALS
    stopservertime();
    stopdrives();
    stopnetwork();
    stopcpu();
    stopmem();
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
    //STOPING ANOTHER INTERCALS
    stopservertime();
    stopsystem();
    stopnetwork();
    stopcpu();
    stopmem();
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
    //STOPING ANOTHER INTERCALS
    stopservertime();
    stopsystem();
    stopdrives();
    stopcpu();
    stopmem();
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
    else {
        if (netdevs == false) {
            $('#netdevs').html(load);
        }
        if (globalip == false) {
            $('#globalip').html(load);
        }
        if (localip == false) {
            $('#localip').html(load);
        }
        if (pinginfo == false) {
            $('#pinginfo').html(load);
        }
    }

}

function cpu() {
    //STOPING ANOTHER INTERCALS
    stopservertime();
    stopsystem();
    stopdrives();
    stopnetwork();
    stopmem();
    var procinfo = false;
    $.ajax({
        type: 'POST',
        url: '/info_aj/procinfo/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>");
            if (j == "running") {
                $('#procinfo').html(load);
            }
            else {
                $('#procinfo').html(j);
                procinfo = true;
            }
        }
    });

    if (procinfo == true) {
        stopcpu();
    }
}

function mem() {
    //STOPING ANOTHER INTERCALS
    stopservertime();
    stopsystem();
    stopdrives();
    stopnetwork();
    stopcpu();
    var memarray = [0, 0, 0, 0, 0, 0, 0];

    $.ajax({
        type: 'POST',
        url: '/info_aj/meminfo/',
        async: false,
        success: function (j) {
            j = j.replace(/\n/g, "<br>");
            if (j == "running") {
                $('#meminfo').html(load);
            }
            else {
                var n = 0;
                var k = 0;
                for (var i = 0; i < j.length; i++) {
                    if (j[i] == " ") {
                        memarray[k] = j.slice(n, i);
                        n = i + 1;
                        k = k + 1;
                    }
                }
                //MEM
                $('#membar').html(membar_ph(memarray[0], memarray[1], memarray[2], memarray[3]));
                $('#memtotal').html((memarray[0] / 1024).toFixed(1));
                $('#memfree').html((memarray[1] / 1024).toFixed(1));
                $('#membuff').html((memarray[2] / 1024).toFixed(1));
                $('#memcach').html((memarray[3] / 1024).toFixed(1));
                $('#memdata').html(((memarray[0] - memarray[1] - memarray[2] - memarray[3]) / 1024).toFixed(1));
                $('#memfree_p').html(((memarray[1] / memarray[0]) * 100).toFixed(1));
                $('#membuff_p').html(((memarray[2] / memarray[0]) * 100).toFixed(1));
                $('#memcach_p').html(((memarray[3] / memarray[0]) * 100).toFixed(1));
                $('#memdata_p').html((((memarray[0] - memarray[1] - memarray[2] - memarray[3]) / memarray[0]) * 100).toFixed(1));
                //SWAP
                $('#swapbar').html(membar_sw(memarray[4], memarray[5]));
                $('#swaptotal').html((memarray[4] / 1024).toFixed(1));
                $('#swapfree').html((memarray[5] / 1024).toFixed(1));
                $('#swapfree_p').html(((memarray[5] / memarray[4]) * 100).toFixed(1));

            }
        }
    });
}

/* TODO MULTIPLE AJAX FUNCTION?
 var globalipinterval = setInterval("globalip();", 200);
 var pinginfointerval = setInterval("pinginfo();", 200);

 function globalip() {
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
 }

 function pinginfo() {
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
 }

 function temp() {
 stopservertime();
 pinginfo();
 globalip();
 }*/