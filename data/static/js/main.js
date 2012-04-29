$.ajaxSetup({
   data: { csrfmiddlewaretoken: '{{ csrf_token }}' },
});

function gedditShowAjaxResponse(responseText, statusText, xhr, $form) { 
    flash(responseText.message);
}

function flash(message) {
    $("#message").html(message);
    $("#messages-container").css({ 'display': 'block' });
    $("#message").effect("highlight", {}, 3000);
}
