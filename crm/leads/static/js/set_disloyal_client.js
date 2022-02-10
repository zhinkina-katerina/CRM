jQuery(document).ready(function() {
     // jQuery("#id_status").change( function() {
         jQuery(document).on( 'change', "#id_is_disloyal", function() {
         const id_is_disloyal = jQuery(this).val();
         const prom_id = jQuery(this).next().val();
         jQuery.ajax({
             url: '/ajax/set_disloyal_client/',
             data: {
                 'is_disloyal': id_is_disloyal,
                 'prom_id': prom_id
             },
         });

     });
 })
jQuery(document).ready(function() {
     // jQuery("#id_status").change( function() {
         jQuery(document).on( 'change', "#id_is_paid_delivery", function() {
         const id_is_disloyal = jQuery(this).val();
         const prom_id = jQuery(this).next().val();
         jQuery.ajax({
             url: '/ajax/set_disloyal_client/',
             data: {
                 'is_paid_delivery': id_is_disloyal,
                 'prom_id': prom_id
             },
         });

     });
 })