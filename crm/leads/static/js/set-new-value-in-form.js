jQuery(function() {
      var form = jQuery("#contactform");
      form.submit(function(e) {
          jQuery("#sendbutton").attr('disabled', true)
          jQuery("#sendwrapper").prepend('<span>Sending message, please wait... </span>')
          jQuery("#ajaxwrapper").load(
              form.attr('action'),
              form.serializeArray(),
              function(responseText, responseStatus) {
                  jQuery("#sendbutton").attr('disabled', false)
              }
          );
          e.preventDefault();
      });
  });
