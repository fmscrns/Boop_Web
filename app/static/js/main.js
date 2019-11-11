$("#ha-secondary-flash-close").click(function() {
    $(".alert").alert("close");
});
$("#ha-primary-flash-close").click(function() {
    $(".alert").alert("close");
});
$(".alert-dismissible").fadeTo(5000, 500).slideUp(500, function(){
    $(".alert-dismissible").alert('close');
});