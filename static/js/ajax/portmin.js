var load = "<img src=/static/img/loading.gif>";
var startsyncinterval = null;
var startupdinterval = null;

$(document).ready(function () {

    //FOR SYNC//
    $sync = $("#portmin_sync");

    $sync.mouseenter(function () {
        $sync.addClass("highlited");
    });

    $sync.mouseleave(function () {
        $sync.removeClass("highlited");
    });

    $sync.click(function () {
        if (!$sync.hasClass("running")) {
            $sync.addClass("running");
            startsetsync();
            startsyncinterval = setInterval(startsync, 1000);
        }
    });

    //FOR UPDATE//
    $upd = $("#portmin_upd");

    $upd.mouseenter(function () {
        $upd.addClass("highlited");
    });

    $upd.mouseleave(function () {
        $upd.removeClass("highlited");
    });

    $upd.click(function () {
        if (!$upd.hasClass("running")) {
            $upd.addClass("running");
            startsetupd();
            startupdinterval = setInterval(startupd, 1000);
        }
    });
});


// FOR SYNC //
function startsetsync() {
    $.ajax({
        type: 'POST',
        url: '/portmin_aj/setsync/',
        success: function (j) {
        }
    });
}

function startsync() {
    $.ajax({
        type: 'POST',
        url: '/portmin_aj/sync/',
        success: function (j) {
            if (j == "running") {
                $("#syncload").html(load);
            }
            else if ((j != "running") && (j != "nothing")) {
                showsyncout(j);
                clearInterval(startsyncinterval);
            }
        }
    });
}

function showsyncout(out) {
    $("#syncout").html(out.replace(/\n/g, "<br>"));
    $("#portmin_sync").removeClass("running");
    $("#syncload").html("Zakończono! Kliknij, by pokazać szczegóły.");
    $("#syncload").click(function () {
        if ($("#syncout").is(":hidden")) {
            $("#syncout").slideDown("slow");
            $("#syncload").html("Zakończono! Kliknij, by schować szczegóły.");
        }
        else {
            $("#syncout").slideUp("slow");
            $("#syncload").html("Zakończono! Kliknij, by pokazać szczegóły.");
        }
    });
}

// FOR UPD //
function startsetupd() {
    $.ajax({
        type: 'POST',
        url: '/portmin_aj/setupd/',
        success: function (j) {
        }
    });
}

function startupd() {
    $.ajax({
        type: 'POST',
        url: '/portmin_aj/upd/',
        success: function (j) {
            if (j == "running") {
                $("#updload").html(load);
            }
            else if ((j != "running") && (j != "nothing")) {
                showupdout(j);
                clearInterval(startupdinterval);
            }
        }
    });
}

function showupdout(out) {
    $("#updout").html(out.replace(/\n/g, "<br>"));
    $("#portmin_upd").removeClass("running");
    $("#updload").html("Zakończono! Kliknij, by pokazać szczegóły.");
    $("#updload").click(function () {
        if ($("#updout").is(":hidden")) {
            $("#updout").slideDown("slow");
            $("#updload").html("Zakończono! Kliknij, by schować szczegóły.");
        }
        else {
            $("#updout").slideUp("slow");
            $("#updload").html("Zakończono! Kliknij, by pokazać szczegóły.");
        }
    });
}

