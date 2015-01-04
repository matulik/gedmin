$(document).ready(function () {
    $(".logtag").click(function () {
        var id = $(this).attr("id");
        var divid = "#" + id + "_cont";
        if ($(divid).is(":hidden")) {
            $(divid).slideDown("slow");
        }
        else {
            $(divid).slideUp("slow");
        }
    });

});