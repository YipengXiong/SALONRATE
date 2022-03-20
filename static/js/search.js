// use ajax to get previous page
function getPrevPage() {
    current_page--
    $("span#current-page").text(current_page)

    if (current_page >= 1) {
        $("a#next-page").show()
        $.ajax({
            type: 'post',
            url: search_url,
            data: {
                'scope': scope,
                'keyword': keyword,
                'current_page': current_page,
                'sort_tag': checked_value,
                'current_sort': current_sort,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (res) {
                // console.log(res)
                $("div.item-container").html(res)
                if (current_page === 1) {
                    $("a#prev-page").hide()
                }
            }
        })
    }
}

// use ajax to get next page
function getNextPage() {
    current_page++
    $("span#current-page").text(current_page)

    if (current_page <= all_page_count) {
        $("a#prev-page").show()
        $.ajax({
            type: 'post',
            url: search_url,
            data: {
                'scope': scope,
                'keyword': keyword,
                'current_page': current_page,
                'sort_tag': checked_value,
                'current_sort': current_sort,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (res) {
                // console.log(res)
                $("div.item-container").html(res)
                if (current_page === parseInt(all_page_count)) {
                    $("a#next-page").hide()
                }
            }
        })
    }
}

// check the checked value in checkbox and store in checked_value dict
function check_checked_value() {
    checked_value = {}
    $("div.tag-filter input:checkbox:checked").each(function () {
        checked_value[$(this).val().toLowerCase().replace(" ", "_")] = 1
    })
}

// document ready functions
$(function () {
    // dynamic add search keyword when switch the search scope
    if (scope === 'salon') {
        $("ul.search-switch li").eq(0).addClass("selected").siblings().removeClass("selected")
        $("input.search-txt").val(keyword)
    } else {
        $("ul.search-switch li").eq(-1).addClass("selected").siblings().removeClass("selected")
        $("input.search-txt").val(keyword)

    }

    // dynamic change the tag filter when switch the search scope
    let current_scope_selected = $(".search-switch li.selected").text().toLowerCase();
    if (current_scope_selected === "service") {
        for (let i = 0; i < 5; i++) {
            $("div.tag-filter li input").eq(i).attr("value", service_tag[i]).attr("id", service_tag[i].toLowerCase())
            $("div.tag-filter li label").eq(i).attr("for", service_tag[i].toLowerCase())
            $("div.tag-filter li label").eq(i).text(service_tag[i])
        }
        $("div.tag-filter li").eq(-1).hide()
    }
    if (current_scope_selected === "salon") {
        let salon_tag = ["Good Env", "Good Service", "Cost Effective", "Good Skill", "Good Attitude", "Not Busy"]
        for (let i = 0; i < 6; i++) {
            $("div.tag-filter li input").eq(i).attr("value", salon_tag[i]).attr("id", salon_tag[i].toLowerCase().replace(" ", "_"))
            $("div.tag-filter li label").eq(i).attr("for", salon_tag[i].toLowerCase().replace(" ", "_"))
            $("div.tag-filter li label").eq(i).text(text_remap(salon_tag[i]))
        }
        $("div.tag-filter li").eq(-1).show()
    }

    // dynamic check the checked value based on the checkbox
    if (current_type) {
        $("div.tag-filter input").eq(current_type).attr("checked", "checked")
        check_checked_value()
    }

    // bind next_page and previous_page function
    $("a#next-page").on('click', getNextPage)
    $("a#prev-page").on('click', getPrevPage)

    // dynamic change the placeholder when change the search scope
    $(".search-switch li").on("click", function () {
        $(this).addClass("selected").siblings().removeClass("selected").end()
        if ($(this).text() === "Salon") {
            $("div.search-box div.search-area input").val("").attr("placeholder", "Salon Name")
        } else {
            $("div.search-box div.search-area input").val("").attr("placeholder", "Service Name")
        }
    })

    // dynamic change the background when click sort
    $(".sort li").on("click", function () {
        $(this).addClass("selected").siblings().removeClass("selected").end()
    })

    // dynamic refresh the page when change the tag
    $(".tag-filter input").change(function () {
        check_checked_value()
        getSearchData()
    })
    // mouse hover to show my center operation
    $("div.my-center").hover(function () {
        $("ul.dropdown-menu").show()
    }, function () {
        $("ul.dropdown-menu").hide()
    })

    // bind sort function on two sort button
    $(".sort li").on("click", sort)


})

// use ajax to refresh the item by selected sort rule
function sort() {
    current_sort = $(this).text().trim().replace("/\s/g", "").toLowerCase()
    current_page = 1
    $.ajax({
        type: 'post',
        url: search_url,
        data: {
            'scope': scope,
            'keyword': keyword,
            'current_page': current_page,
            'sort_tag': checked_value,
            'current_sort': current_sort,
            'csrfmiddlewaretoken': csrf_token
        },
        success: function (res) {
            // console.log(res)
            $("span#current-page").text(current_page)
            $("div.item-container").html(res)
        }
    })
}

// remap the words
function text_remap(original_name) {
    switch (original_name) {
        case ("Good Env"):
            return "Nice Environment"
        case("Good Service"):
            return "Attentive Service"
        case("Good Skill"):
            return "Excellent Skill"
        case("Good Attitude"):
            return "Warm Attitude"
        case("Cost Effective"):
            return "Cost Effective"
    }
}

// use ajax to get item data, return ajax_search.html(item content)
function getSearchData() {
    let scope = $('ul.search-switch li.selected').text().toLowerCase()
    let keyword = $('input.search-txt').val()
    current_page = 1
    $.ajax({
        type: 'post',
        url: ajax_search_url,
        data: {
            'scope': scope,
            'keyword': keyword,
            'sort_tag': checked_value,
            'current_page': current_page,
            'current_sort': current_sort,
            'csrfmiddlewaretoken': csrf_token
        },
        success: function (res) {
            $("div.item-container").html(res)
            if (res.trim() === "") {
                $("span#current-page").text(0)
                $("span#all-page").text(0)
                $("a#next-page").hide()
                $("a#prev-page").hide()
            } else {
                $("span#current-page").text(current_page)
                $("a#next-page").show()
                if (current_page >= parseInt(all_page_count)) {
                    $("a#next-page").hide()
                }
                if (current_page === 1) {
                    $("a#prev-page").hide()
                }
            }
        }
    })
}

// change the tag filter checkbox when change the search scope
$(function () {
    $(".search-switch li").on("click", function () {
        $(this).addClass("selected").siblings().removeClass("selected").end()
        let scope = $(this).text().toLowerCase()
        if (scope === "service") {
            for (let i = 0; i < 5; i++) {
                $("div.tag-filter li input").eq(i).attr("value", service_tag[i]).attr("id", service_tag[i].toLowerCase())
                $("div.tag-filter li label").eq(i).attr("for", service_tag[i].toLowerCase())
                $("div.tag-filter li label").eq(i).text(service_tag[i])
            }
            $("div.tag-filter li").eq(-1).hide()
        }
        if (scope === "salon") {
            let salon_tag = ["Good Env", "Good Service", "Cost Effective", "Good Skill", "Good Attitude", "Not Busy"]
            for (let i = 0; i < 6; i++) {
                $("div.tag-filter li input").eq(i).attr("value", salon_tag[i]).attr("id", salon_tag[i].toLowerCase().replace(" ", "_"))
                $("div.tag-filter li label").eq(i).attr("for", salon_tag[i].toLowerCase().replace(" ", "_"))
                $("div.tag-filter li label").eq(i).text(text_remap(salon_tag[i]))
            }
            $("div.tag-filter li").eq(-1).show()
        }
        $("div.tag-filter input[type=checkbox]").prop("checked",false)
        check_checked_value()
    })
})

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