$(document).ready(function() {
    $('#admin-datatable').DataTable( {
        // "searching": false,
        // 'showing' :false,
        "scrollX": true,
        "lengthMenu": [[14, 30, 60, -1], [14, 30, 60, "All"]],
        "order": [[ 3, "desc" ]]
    } );
} );