$(".form-check-input").change(function() {
  $(this).parent().hide();
  $(this).parent().next().removeClass("hide");
  $(this.form).submit(function SubForm(e) {
    e.preventDefault();
    $.ajax({
      url: '/substitute/listing/',
      type: 'post',
      data: $(this).serialize(),
      success: function() {}
    });
  });
  $(this.form).submit();
});
