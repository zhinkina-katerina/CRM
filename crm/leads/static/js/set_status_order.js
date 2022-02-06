jQuery(document).ready(function() {
     jQuery("#id_status").change( function() {
         const status_id = jQuery(this).val();
         const prom_id = jQuery("#prom_id").val();
         jQuery.ajax({
             url: '/ajax/set_status_order/',
             data: {
                 'status_id': status_id,
                 'prom_id': prom_id
             },
         });

     });
 })