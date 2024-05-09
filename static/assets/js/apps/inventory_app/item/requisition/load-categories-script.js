$(document).ready(function() {
    // Function to load categories
    function loadCategories() {
        $.ajax({
            url: '/ajax_datatable/item_category/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // Clear the dropdown
                $('#item-category').empty();

                // Add "All" option to the dropdown
                $('#item-category').append('<option value="">All Categories</option>');

                // Add categories to the dropdown
                data.data.forEach(function(category) {
                    $('#item-category').append(
                        '<option value="' + category.id + '">' + category.name + '</option>'
                    );
                });
            }
        });
    }

    // Load categories when the page loads
    loadCategories();
});
