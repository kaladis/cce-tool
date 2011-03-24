$(document).ready(function(){
    $('a.del').bind('click',function(e){
        if (! confirm('Are you sure you want to delete the marks? !! This will delete all the marks for that year, section and subject combination (FA1,FA2,SA2,FA3,FA4,SA2)....  It is OK?')) return false;
        url = $(this).attr('href');
        e.preventDefault();
        var el = $(this);
        $.ajax({
            url:url,
            type:'GET',
            dataType:'json',
            success:function(res,text){
                if(res.done == false) {  alert ('Not delete properly'); return false;}
                $(el).closest('tr').fadeOut();
            }
        });
    });

});