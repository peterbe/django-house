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
    .append($('<img alt="Preview" width="70">').attr('src', thumbnail))
    .appendTo(row);
  $('<td></td>')
    .append($('<span>').text(name))
    .appendTo(row);
  $('<td></td>')
    .append($('<span>').text(humanFileSize(size)))
    .appendTo(row);
  row.appendTo(container);
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
      $.each(InkBlobs, function(i, InkBlob) {
        console.log('BLOB', InkBlob);
        filepicker.convert(InkBlob, {width: 70, height: 70}, function(metadata) {
          console.log('   METADATA', metadata);
          make_preview_field_row(container, InkBlob.url, InkBlob.filename, InkBlob.size, metadata.url);
        });
      });
      $('form.upload:hidden').show();
    },
    function(FPError){
      console.log(FPError.toString());
    }
  );

}

$(function() {
  $('button.open-filepicker').click(open_filepicker);
});
