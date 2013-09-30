$(function() {

  $('#photo-edit button.pure-button-primary').click(function() {
    $('#photo-edit form').submit();
  });


  function _start_loading() {
    $('#photo-edit button').hide();
    $('#photo-edit img').show();
  }
  function _stop_loading() {
    $('#photo-edit img').hide();
    $('#photo-edit button').show();
  }

  var _submitted = false;
  $('#photo-edit form').submit(function() {
    if (_submitted) return false;
    _submitted = true;  // todo, accompany this with a big nice spinner
    _start_loading();
    console.log('SUBMIT');
    var form = $(this);
    var id = form.data('id');
    var data = {};
    data.description = $('input[name="description"]', form).val();
    data.coverphoto = $('input[name="coverphoto"]', form).prop('checked');
    data.csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]', form).val();
    console.log('DATA', data);
    var req = $.post(location.pathname + id + '/', data);
    req.done(function(response) {
      //$('#photo-edit').modal('hide');
      location.href = location.pathname;
      _submitted = false;
    });
    req.fail(function() {
      _stop_loading();
      alert("An error happened when trying to save. Try again later.");
      _submitted = false;
    });
    $('#photo-edit').modal('show');
    return false;
  });

  $('.photo-box a.edit').click(function() {
    var id = $(this).data('id');
    var req = $.getJSON(location.pathname + id + '/');
    var container = $('#photo-edit');
    $('form', container).data('id', id);
    req.done(function(response) {
      $('.modal-thumbnail img', container).remove();
      $('<img>')
        .attr('src', response.thumbnail.url)
        .attr('width', response.thumbnail.width)
        .attr('height', response.thumbnail.height)
        .appendTo($('.modal-thumbnail', container));
      if (response.description) {
        $('input[name="description"]', container).val(response.description);
      } else {
        $('input[name="description"]', container).val('');
      }
      $('input[name="coverphoto"]', container).prop('checked', response.is_cover_photo);
      $('#photo-edit').modal('show');
      setTimeout(function() {
        if (!$('#photo-edit input[name="description"]').val()) {
          $('#photo-edit input[name="description"]').focus();
        }
      }, 100);
    });
    req.fail(function() {
      alert("Unable to edit that photo.");
      location.href = location.pathname;
    });

    return false;
  });

  if (location.hash.search(/#id-\d/) > -1) {
    if ($(location.hash).length === 1) {
      $('a.edit', location.hash).click();
    }
  }
});
