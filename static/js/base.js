// get search scope, salon or service
$(function getSearchScope() {
    $(".search-switch li").on("click", function () {
        $(this).addClass("selected").siblings().removeClass("selected").end()
        $("input.dynamic-scope").val($(this).text().toLowerCase())
    })
})

// form submit
function getSearchData() {
    $("form#search-form").submit()
}

// bind ENTER key to search function
$(function search() {
    $('input.search-txt').keydown(function (e) {
        if (e.keyCode === 13) {
            getSearchData()
        }
    })

    // bind search icon to search function
    $(".search-btn").on("click", getSearchData)
})

$(function () {
    $("div.my-center").hover(function() {
        $("ul.dropdown-menu").show()
    },function (){
        $("ul.dropdown-menu").hide()
    })
})