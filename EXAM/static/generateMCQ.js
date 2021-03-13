$(document).ready(function () {
    load();
});

function load() {
    $("#btn_course_code").focus();
    $("#exam_topic").focus();


    $("#btn_course_code").click(function(){
        $('#exam_topic').empty();
        var code =$('#course_code').val();
        var lessons =$('#exam_topic');
    
    fetch(`/mcqUpload_lesson_selection_load?c=${code}`).then(function(response){
        response.json().then(function(lesson_array){
            var optionHTML='';
            for (var i = 0; i < lesson_array.length; i++) {
                optionHTML+=`<option value="${lesson_array[i]}">${lesson_array[i]}</option>`;
                console.log(optionHTML);
            }
            lessons.append(optionHTML);
        });
    });

});
}