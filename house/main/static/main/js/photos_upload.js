// http://stackoverflow.com/a/14919494/205832
function humanFileSize(bytes, si) {
    var thresh = si ? 1000 : 1024;
    if(bytes < thresh) return bytes + ' B';
    var units = si ? ['kB','MB','GB','TB','PB','EB','ZB','YB'] : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while(bytes >= thresh);
    return bytes.toFixed(1)+' '+units[u];
};

function make_preview_field_row(container, url, name, size, thumbnail) {
  var row = $('<tr></tr>');
  $('<td></td>')
    .append($('<input type="checkbox" name="urls" checked>').val(url))
    .appendTo(row);
  $('<td></td>')
    .append($('<img alt="Preview">')
            .attr('src', thumbnail))
    .appendTo(row);
  $('<td></td>')
    .append($('<span>').text(name))
    .appendTo(row);
  $('<td></td>')
    .append($('<span>').text(humanFileSize(size)))
    .appendTo(row);
  row.appendTo(container);
}


function add_preview_field_url(container, url, thumbnail) {
  $('tr').each(function(i, row) {
    if ($('input[name="urls"]', row).val() == url) {
      $('img', row).attr('src', thumbnail);
    }
  });
}


function open_filepicker() {
  var opts = {
      mimetypes: ['image/jpeg', 'image/png'],
      container: 'window',
      services:['COMPUTER', 'FACEBOOK', 'GMAIL'],
  }
  filepicker.pickMultiple(
    opts,
    function(InkBlobs){
      console.log(InkBlobs);
      var container = $('form.upload tbody');
      var placeholder_url = container.data('placeholder-url');
      (new Image()).src = placeholder_url;  // preloading

      $.each(InkBlobs, function(i, InkBlob) {
        //console.log('BLOB', InkBlob);
        make_preview_field_row(container, InkBlob.url, InkBlob.filename, InkBlob.size, placeholder_url);
        filepicker.convert(InkBlob, {width: 60, height: 60}, function(metadata) {
          //console.log('   METADATA', metadata);
          add_preview_field_url(container, InkBlob.url, metadata.url, 60);

        });
      });
      $('form.upload:hidden').show();
    },
    function(FPError){
      // TODO needs a lot more work
      console.log(FPError.toString());
    }
  );

}

$(function() {
  $('button.open-filepicker').click(open_filepicker);
  if ($('input[name="open_filepicker_automatically"]').size()) {
    Remember.get('open_filepicker_automatically', false, function(value) {
      $('input[name="open_filepicker_automatically"]').attr('checked', 'checked');
      $('button.open-filepicker').click();
    });
  }

  $('input[name="open_filepicker_automatically"]').on('change', function() {
    Remember.set('open_filepicker_automatically', this.checked);
  });

});
