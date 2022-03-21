$(function () {
    $("div.row-cols-auto>div>div").each(function () {
        console.log('click')
        $(this).on("click", getType)
    })
})

function getType() {
    let current_type = $(this).attr("data-id")
    let form = $('<form></form>');
    form.attr('action', homepage_search_url);
    form.attr('method', 'post');
    form.attr('target', '_self');

    let keyword_input = $('<input type="text" name="keyword" />');
    keyword_input.attr('value', '');

    let scope_input = $('<input type="text" name="scope" />');
    scope_input.attr('value', 'service');

    let type_input = $('<input type="text" name="current_type" />');
    type_input.attr('value', current_type);

    let csrf_input = $('<input type="text" name="csrfmiddlewaretoken" />');
    csrf_input.attr('value', homepage_csrf_token);

    form.append(csrf_input)
    form.append(scope_input)
    form.append(keyword_input)
    form.append(type_input);
    form.appendTo("body")

    form.submit();
}
