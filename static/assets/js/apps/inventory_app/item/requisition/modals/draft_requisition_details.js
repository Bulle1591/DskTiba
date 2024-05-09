function showDraftRequisitionDetails(element) {
    var id = $(element).data('id');
    $.ajax({
        url: '/draft_requisitions/' + id + '/details/',
        method: 'GET',
        success: function(data) {
            // Populate the modal with the returned data
            $('#requisitionPreviewModal .modal-body').html(data);
            // Show the modal
            $('#requisitionPreviewModal').modal('show');
        }
    });
}
