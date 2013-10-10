$(function() {
  $('form.search input').keypress(function() {
    console.log($(this).val());
  });
});
