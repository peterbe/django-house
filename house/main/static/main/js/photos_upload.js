$(function() {
  filepicker.pick({
     mimetypes: ['image/jpeg', 'image/png'],
    //container: 'window',
    services:['COMPUTER', 'FACEBOOK', 'GMAIL'],
  },
                  function(InkBlob){
                    console.log(JSON.stringify(InkBlob));
                  },
                  function(FPError){
                    console.log(FPError.toString());
                  }
                 );
});
