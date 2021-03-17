$(document).ready(function () {
    load();
});

function load() {
    $('#btn_course_code').focus();
    $('#lessons_table').focus();
    $('#lesson_name').focus();
    $('#btnAdd').focus();

    
    $('#btnAdd').click(function(){
        //$('#addcard').empty();
        var addDiv= $('#addcard');
        var template='';
        template+='<div class="card" style="width: 25rem;">'+
        '<ul class="list-group list-group-flush">'+
            '<li class="list-group-item">'+
            
            '<label class="custom-control-label">Course Outcome </label><br/>'+
            '<input name="exam_CLO" id="exam_CLO"  type="text" class="custom-radio"></li>'+
            '<li class="list-group-item">'+
                
                '<label class="custom-control-label">Syllabus/Topic/lesson :</label><br/>'+
               '<input id="exam_topic" list="lesson_name" name="exam_topic" class="custom-select custom-select-md mb-3 btn-outline-info " placeholder="Enterthe exact name of lesson" aria-label=".custom-select-lg example">'+
                '<datalist id="lesson_name">'+
                   '<option selected disabled>Enter the exact name of lesson</option>'+
                '</datalist></li>'+
            '<li class="list-group-item">'+
                '<label class="custom-control-label">Question Complexity Level</label>'+
                '<select class="custom-select-sm btn-outline-info" id="inputGroupSelect04" name="complex_level aria-label="Example select with button addon" required>'+
                '<option selected disabled="disabled">Select Complex level</option>'+
                '<option value="1">Low</option>'+
                '<option value="2">Medium</option>'+
                '<option value="3">High</option>'+
               '<option value="5">Very High</option>'+
                '<option value="10">Insane</option>'+
                '</select></li>'+
            '<li class="list-group-item">'+
           
            '<label class="custom-control-label">Number of Questions :</label><br/>'+
            '<input id="exam_total_questions" name="exam_total_questions" type="text" class="custom-radio"></li>'+
        '</ul>'+
    '</div>';
    addDiv.append(template);

    });


    $("#btn_course_code").click(function(){
        $('#lessons_table').empty();
        var code =$('#course_code').val();
        var lessons_table =$('#lessons_table');
        var lessons =$('#lesson_name');
        
    
    fetch(`/mcqUpload_lesson_selection_load?c=${code}`).then(function(response){
        response.json().then(function(lesson_array){
            var viewHTML='';
            var optionHTML='';
            for (var i = 0; i < lesson_array.length; i++) {
                viewHTML+=`<td class="col">Lesson_no :${lesson_array[i]}</td>`;
                optionHTML+=`<option value="${lesson_array[i]}">${lesson_array[i]}</option>`;
                console.log(optionHTML);
            }
            lessons_table.append(viewHTML);
            lessons.append(optionHTML);
            
        });
    });

});
}