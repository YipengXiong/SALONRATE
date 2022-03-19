$(document).ready(function () {
    // Click "Write a comment", show the comment form
    $("#mac").click(function () {
        $("#mac").toggle();
        $(".cmf").toggle(100);
    })
    // Click "Cancel", hide the comment form 
    $("#cancel").click(function () {
        $("#mac").toggle();
        $(".cmf").toggle(100);
    })
    // Click a star, transfer the value to the "star" field in the comment form 
    $(".star-rate > label").click(function () {
        var rate = $(this).val();
        $(".star-rate > label").removeClass("rated")
        for (let i = 0; i < rate; i++) {
            $(".star-rate > label.class" + rate).addClass("rated")
        }
        $("#id_star").val(rate);
    })

    // Click the solid heart to unfollow
    $(".followed").click(function () {

    })
    // Click the empty heart to follow
    $(".unfollowed").click(function () {

    })
});

// $.ajax({
//     type:'POST',
//     url:'',
//     data:{
//         'scrfmiddlewaretoken':'',
//     }
// })
$("div.star-rate label").on("click", function () {
    let current_star = $(this).text()
    // console.log(current_star)
    $("div.star-rate label").removeClass("rated")
    for (let i = 0; i < current_star; i++) {
        $("div.star-rate label.star" + i).addClass("rated")
    }
    $("input#id_star").val(current_star)
})

