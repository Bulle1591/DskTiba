function loadRoles() {
    $.ajax({
        url: '/ajax_card/role/', // replace with your API endpoint
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var roleContainer = $('#roleContainer'); // replace with your container ID
            roleContainer.empty(); // clear the container

            // loop through the data and create the cards
            $.each(data, function(index, role) {
                var permissions = role.permissions.slice(0, 4);
                var morePermissionsCount = Math.max(role.permissions.length - 4, 0);
                var card = `
                    <div class="col-xl-4 col-lg-6 col-md-6">
                        <div class="card role-permission-card">
                          <div class="card-body">
                            <div class="d-flex justify-content-between mb-2">
                              <h6 class="fw-normal">Total ${role.total_users} users</h6>
                              <ul class="list-unstyled d-flex align-items-center avatar-group mb-0">`;
                                // loop through the users in the role
                                $.each(role.users, function(index, user) {
                                    card += `
                                        <li data-bs-toggle="tooltip" data-popup="tooltip-custom" data-bs-placement="top" title="<span class="math-inline">\{user\.full\_name\}" class\="avatar avatar\-sm pull\-up"\>
<img class="rounded-circle" src\="/media/</span>{user.image_url}" alt="Avatar" onerror="this.src='/path/to/default-image.png'">  </li>
                                    `;
                                });

                                card += `
                          </ul>
                        </div>
                        <div class="d-flex justify-content-between align-items-end">
                          <div class="role-heading">
                            <h4 class="role-name mb-1"><span class="math-inline">\{role\.name\}</h4\>
<h6 class="role-description" style\="display: none;"\></span>{role.description}</h6>
                            <a href="javascript:void(0);" class="edit-role me-5" data-bs-toggle="modal" data-bs-target="#addRoleModal" data-role-id="<span class="math-inline">\{role\.id\}" data\-role\-permissions\='</span>{JSON.stringify(role.permissions)}'><small>Edit Role</small></a>
                            <a href="/role/view/${role.id}/"><small>View Role</small></a>
                          </div>
                          <a href="javascript:void(0);" class="text-muted">
                              ${permissions.join(', ')}
                              ${morePermissionsCount > 0 ? ' (+ ' + morePermissionsCount + ')' : ''}
                          </a>
                        </div>
                      </div>
                    </div>
                `;
                roleContainer.append(card);
            });

        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error loading roles:", textStatus,
// Call the function when the page loads
$(document).ready(function() {
    loadRoles();
});