$(document).ready(function(){
    $('#marksform').ajaxForm({
        target: '#marks',
    });
    $('a#closeeditform').live('click',null,function(e){
        e.preventDefault();
        $('#markeditpanel').fadeOut();
    });
});