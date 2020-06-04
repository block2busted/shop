$(document).off('click').on('click', '#add-to-cart', function (event) {
    event.preventDefault();
    $.ajax({
        data: $(this).serialize(),
        type: 'get',
        url: $(this).attr('href'),
        success: function (data) {
            $('#cart-detail').html(data['reload_cart'])
            console.log(data);
            console.log('success');
        },
        error: function (data) {
            console.log(data);
            console.log('error');
        }
    })
})