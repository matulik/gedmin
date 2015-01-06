$(document).ready(function () {
    $(".logtag").click(function () {
        var $tag = "#" + $(this).attr("id") + "_cont";
        if ($($tag).is(":hidden")) {
            console.log($tag);
            $($tag).slideDown("slow");
            $(this).addClass("logtaghl");
        }
        else {
            $($tag).slideUp("slow");
            $(this).removeClass("logtaghl");
        }

    });
});