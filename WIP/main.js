// Use on <li>
$.fn.playCard = function playCard() {
    if ($(this).children("img").hasClass("face-up") === false) {
        // console.log("showed!");
        $(this).children("img").addClass("face-up");
        $(this).children("span").html("1");
        $("#dec").html(parseInt($("#dec").html()) + parseInt($(this).children('img').attr('value')));


    } else {
        // console.log("hide!");
        $(this).children("img").removeClass("face-up");
        $(this).children("span").html("0");
        $("#dec").html(parseInt($("#dec").html()) - parseInt($(this).children('img').attr('value')));
    }


};

function makeCards(size = 8) {
    size = parseInt(size);

    // output images then hide them
    var output = "<h2>Jak funguje binární soustava?</h2>";
    output += "<ol>";

    for (let i = size; i >= 0; i--) {
        output += '<li id="li' + String(Math.pow(2, i)) + '">';
        output += "<img src = 'pics/" + String(Math.pow(2, i)) + ".png' value='" + String(Math.pow(2, i)) + "' class='face-up' />";
        output += "<span>1</span>";
        output += "</li>";
    }
    output += "</ol>";

    // output += "<div id='values'>";
    output += "<span> V desítkové soustavě </span>";
    output += "<span id='dec'></span>";
    // output += "<span id='bin'></span>";
    // output += "</div>";
    document.getElementById("main").innerHTML = output;
    // console.log("Cards placed")
}

function initialize() {
    makeCards();

    $("li").click(function() {
        $(this).playCard();
    });

    $("#dec").html(511);
    // $("#bin").html(1);

}

// console.log("start");
//
//
initialize();