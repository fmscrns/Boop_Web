function readURL(input, previewCont) {
    if ((input.files.length === 1) && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function (e) {
            $(previewCont).attr("src", e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]);
    }
    else if((input.files.length > 1) && input.files[0]) {
        var filesAmount = input.files.length;

        for (i = 0; i < filesAmount; i++) {
            let reader = new FileReader();
            
            reader.onload = function(event) {
                $($.parseHTML("<img>")).attr("src", event.target.result).appendTo(previewCont);
            }

            reader.readAsDataURL(input.files[i]);
        }
    }
}
$("#pet_profPic_input").change(function(){
    readURL(this, "#pet-profpic-preview");
});
$("#pet_coverPic_input").change(function(){
    readURL(this, "#pet-coverpic-preview");
});
$("#user_profPhoto_input").change(function(){
    readURL(this, "#user-profpic-preview");
});
$("#user_coverPhoto_input").change(function(){
    readURL(this, "#user-coverpic-preview");
});
$("#sharePhoto_input").change(function(){
    readURL(this, "#post-sharephoto-preview");
});

function showImageCol(col_id) {
    document.getElementById(col_id).style.display = "block";
}

$("#ha-secondary-flash-close").click(function() {
    $(".alert").alert("close");
});
$("#ha-primary-flash-close").click(function() {
    $(".alert").alert("close");
});
$(".alert-dismissible").fadeTo(5000, 500).slideUp(500, function(){
    $(".alert-dismissible").alert("close");
});

$("#commentPost_input").attr("aria-describedby","button-addon2");