$(document).ready(function(){
    $('a.editmark').bind('click', function(e){
        e.preventDefault();
        var url=$(this).attr('href');
        $.ajax({
          url:url,
          type:'GET',
          dataType:'html',
          success: function(data,status){
            $('#editmarkform').html(data).find('#markeditform').ajaxForm({
                dataType:'json',
                success:function(data,status){
                    if(data.status == true){
                      var row = $('#'+data.id);
                      $.each(data.fields, function(i,j){
                          $(row).find("."+i).text(j);
                       });
                      $(row).css('font-weight','bold');
                    }
                 }
             });
          }
        });
     });
});
