$(document).ready(function () {
    load();
});

function load() {
    $('#btn_course_code').focus();
    $('#lessons_table').focus();
    $('#lesson_name').focus();
    $('#btnAdd').focus();
    $('#linked_course_code').focus();



    var check=$('#linked_course_code').attr('value');
    //console.log(check)
    if (check!= 'teacher')
    {

        $('#lessons_table').empty();
        $('#clo').empty();
        var clos =$('#clo');
        var code = check;
        var lessons_table =$('#lessons_table');
        var lessons =$('#lesson_name');
        
    
    fetch(`/generateMCQ_lesson_load?c=${code}`).then(function(response){
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

    fetch(`/generateMCQ_clo_load?c=${code}`).then(function(response){
        response.json().then(function(clo_array){
            var optionHTML='';
            for (var i = 0; i < clo_array.length; i++) {
                optionHTML+=`<option value="${clo_array[i]}">${clo_array[i]}</option>`;
                console.log(optionHTML);
            }
            clos.append(optionHTML);
        });
    });
    }






    $("#btn_course_code").click(function(){
        $('#exam_topic').empty();
        $('#lessons_table').empty();
        $('#clo').empty();
        var clos =$('#clo');
        var code =$('#course_code').val();
        var lessons_table =$('#lessons_table');
        var lessons =$('#lesson_name');
        
    
    fetch(`/generateMCQ_lesson_load?c=${code}`).then(function(response){
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
    fetch(`/generateMCQ_clo_load?c=${code}`).then(function(response){
                response.json().then(function(clo_array){
                    var optionHTML='';
                    for (var i = 0; i < clo_array.length; i++) {
                        optionHTML+=`<option value="${clo_array[i]}">${clo_array[i]}</option>`;
                        console.log(optionHTML);
                    }
                    clos.append(optionHTML);
                });
            });

});














    $('#btnAdd').click(function(){
        //$('#addcard').empty();
        var addDiv= $('#addcard');
        var template='';
        // var check=('#linked_course_code').val();
        // console.log(check)
        template+=`<div class="card" style="width: 22rem;">
        <ul class="list-group list-group-flush">
            <li class="list-group-item">
            <label class="form-control-label h5">Course Outcome </label><br/>
            
            <input id="exam_CLO" list="clo" name="exam_CLO" 
            class="custom-select form-select custom-select-md mb-3 btn-outline-info "
            placeholder="Select CLO"
            autocomplete="off"
            aria-label=".custom-select-lg example">
                <datalist id="clo">
                    <option selected disabled>Enter the exact name of lesson</option>
                </datalist></li>


    </li>

            <li class="list-group-item">
                <label class="form-control-label h5">Syllabus/Topic/lesson :</label><br/>
                <input id="exam_topic" list="lesson_name" name="exam_topic" class="custom-select form-select custom-select-md mb-3 btn-outline-info " placeholder="Select lesson"
                autocomplete="off"
                aria-label=".custom-select-lg example">
                <datalist id="lesson_name">
                    <option selected disabled>Select lesson</option>
                </datalist></li>
            <li class="list-group-item">
                <label class="form-control-label h5">Question Complexity Level</label>
                <select
                    class="custom-select form-select btn-outline-info"
                    id="inputGroupSelect04"
                    name="complex_level"
                    aria-label="Example select with button addon"
                    required>
                <option selected disabled="disabled">Select level</option>
                <option value="1">Low</option>
                <option value="2">Medium</option>
                <option value="3">High</option>
                <option value="5">Very High</option>
                <option value="10">Insane</option>
                </select></li>
                <li class="list-group-item">
                     <label class="form-control-label h5"> Total_marks </label>
                       <input type="number" class="input-group form-control" id="marks" name="marks" 
                       placeholder="For this Lesson" /></div>
                        </li>
        </ul>
    </div>`;
    addDiv.append(template);

    });





}