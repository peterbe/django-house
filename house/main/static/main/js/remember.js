var Remember = (function() {
  var storage = navigator.storage ||          // New API, new object
                navigator.alsPolyfillStorage; // Where the polyfill lives

  return {
     set: function(key, value, callback) {
       storage.set(key, value).then(function() {
         if (callback) callback();
       });
     },
     get: function(key, default_, callback) {
       storage.get(key).then(function(value) {
         callback(value);
       }, function() {
         callback(default_);
       });
     }
  };

})();
