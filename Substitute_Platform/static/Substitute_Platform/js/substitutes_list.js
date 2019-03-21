
$(".form-check-input").change(function () {
  $(this).parent().hide();
  $(this).parent().next().removeClass("hide");
  $(this.form).submit(function SubForm (e){
    e.preventDefault();
    $.ajax({
      url:'/substitute/listing/',
      type:'post',
      data:$(this).serialize(),
      success:function(){
      }
    });
  });
  $(this.form).submit();
});


//
//     if (this.checked) {
//       toHide = "#cb1";
//       console.log("#cb" + i);
//       toShow = "#textsaved-" + i;
//       toSubmit = "#save-" + i;
//       $(toHide).hide();
//       $(toShow).show();
//       $(this.form).submit(function SubForm (e){
//         e.preventDefault();
//         $.ajax({
//           url:'/substitute/listing/',
//           type:'post',
//           data:$(this).serialize(),
//           success:function(){
//           }
//         });
//       });
//       $(this.form).submit();
//     }
//   });
//   i++;
// }
