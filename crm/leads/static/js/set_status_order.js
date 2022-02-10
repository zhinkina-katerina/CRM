jQuery(document).ready(function() {
         jQuery(document).on( 'change', "#id_status", function() {
         const status_id = jQuery(this).val();
         const prom_id = jQuery(this).next().val();
         jQuery.ajax({
             url: '/ajax/set_status_order/',
             data: {
                 'status_id': status_id,
                 'prom_id': prom_id
             },

         });

     });
 })