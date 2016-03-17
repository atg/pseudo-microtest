$(function () {
    $('.statuses').on('click', function (event) {
        var results = $(event.target).parent().next('tr');
        var languages = results.next('tr');
        var display = results.css('display');
        if (display == 'none') {
            results.show();
            languages.show();
        } else {
            results.hide();
            languages.hide();
        }
    })
})
