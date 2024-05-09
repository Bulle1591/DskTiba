$('.detail-item').click(function() {
    var itemId = $(this).data('id');  // Get the item id from the data-id attribute

    // Fetch the item data (replace '/get-item/' with the actual URL of your view)
    $.get('/get-item/', {id: itemId}, function(data) {
        // Populate the detail fields with the item data
        $('#detail-modal .name').text(data.name);
        // Add other fields as needed...

        // Show the modal
        $('#detail-modal').modal('show');
    });
});
