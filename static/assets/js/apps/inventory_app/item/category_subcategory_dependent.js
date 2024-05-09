$(document).ready(function () {
    // Hide the 'Pharmaceutical-Fields' div by default
    $('#Pharmaceutical-Fields').hide();

    $('#id_category').change(function () {
        var url = $("#itemForm").attr("data-item-subcategories-url");  // get the url of the 'load_subcategories' view
        var categoryName = $('#id_category option:selected').text();  // get the selected category name from the HTML input

        // Show the 'Pharmaceutical-Fields' div if 'Pharmaceuticals' is selected
        if (categoryName == 'Pharmaceuticals') {
            $('#Pharmaceutical-Fields').show();
        } else {
            $('#Pharmaceutical-Fields').hide();
        }

        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= '/ajax/load-subcategories/')
            data: {
                'category_id': $(this).val()       // add the category id to the GET parameters
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
