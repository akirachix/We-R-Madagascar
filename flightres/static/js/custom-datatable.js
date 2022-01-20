$(document).ready(function() {
    $('#admin-datatable').DataTable( {
        // "searching": false,
        // 'showing' :false,
        "scrollX": true,
        "lengthMenu": [[10, 20, 50, -1], [10, 20, 50, "All"]],
        "order": [[ 0, "desc" ]]
    } );
} );