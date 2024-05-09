$(document).ready(function () {
    $('#id_category').change(function () {
        var url = $("#equipmentForm").attr("data-equipment-subcategories-url");  // get the url of the 'load_subcategories' view
        var categoryId = $(this).val();  // get the selected category ID from the HTML input

        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= '/ajax/load-subcategories/')
            data: {
                'category_id': categoryId       // add the category id to the GET parameters
            },
            success: function (data) {
                var options = '<option value="">---------</option>';  // start with the default option
                for (var i = 0; i < data.length; i++) {
                    options += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
                }
                $("#id_subcategory").html(options);
            }

        });

    });
});
