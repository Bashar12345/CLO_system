$(document).ready(function () {
    load();
});

function load() {
    //alert("Is it working");
    $("#total").focus();
    $("#options").focus();
    $("#btn_course_title").focus();
    $("#course_code").focus();


    $("#btn_course_title").click(function(){
        $('#course_code').empty();
        var course = $("#course_title").val();
        var code =$("#course_code");
        var len =0
        //var lessons =$('#lesson');
        //alert("" + course);
            fetch(`/mcqUpload_course_code_selection_load?c=${course.replace(/\s+/g, ';')}`).then(function(response){
                response.json().then(function(route_data){
                    var option_code_HTML='';
                    //var option_lesson_HTML='';
                    
                    for (var i = 0; i < route_data.length; i++) {
                        option_code_HTML+=`<option value="${route_data[i].course_code}">${route_data[i].course_code}</option>`;
                        //option_lesson_HTML+=`<option value="${route_data[i].course_lessons}">${route_data[i].course_lessons}</option>`;
                        //console.log(optionHTML)
                        //console.log(option_lesson_HTML)
                        
                    }
                    code.append(option_code_HTML);
                    len++
                    //lessons.append(option_lesson_HTML);

                });
    });
});

for (var i = 0; i < len; i++) {

}
    $("#course_code").change(function(){
        $('#lesson').empty();
        var code =$("#course_code").val();
        var lessons =$('#lesson');
    
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

    $("#total_btn").click(function(){
        $('#addQuestion').empty();
        var total_questions = $("#total").val();
        var options = $("#options").val();
        //alert("" + total_questions);

        if (total_questions > 0) {
            createTable(total_questions,options);
        }

    });

}

        function createTable(total_questions,options) {
            var inputTable="";
            var count =1;
            inputTable =`<div class="container">`;

for (let i = 0; i <total_questions; i++) {
    inputTable += `  <div>
    <label class="form-control-label" for="question-${i + 1}"><br/>
    <h4>Question ${i + 1}:</h4>
    </label>
</div>
<div>
<input class="form-control" id="question-'+ i +'" name="question" type="text"
    placeholder="EnterQuestion-${i + 1}" /><br/>
</div>`;
inputTable += `<label class="form-control-label" ><h5>MCQ-${i + 1} Answer:</h5></label><br/>`;
    inputTable += `<input class="form-control" type="text" id="answer" name="answer${i}" 
        placeholder="Enter Answer-${i + 1}">`;

        inputTable +=  `<div class="row"><br/>`;
for (let j = 0; j < options; j++) {
    
    inputTable +=`<div class="input-group mb-3"><label>Option-${j+1}:</label><br>`;

    inputTable +=`<div class="input-group-append mb-3"><input type="text" id="options" name="op[${j+count}]" placeholder="Enter Option-${j+1}"></div><br/>`;
    if(j==1){
        inputTable += `<div class="w-100"></div>`;
    } 
    inputTable += `</div>`;
        count++;
    
} 
        inputTable += `</div>`;
        }

        $('#addQuestion').append(inputTable);
    }  




    /*$('#add').click(function(){
    var formData = new FormData();
           // for (let i = 0; i < total_questions; i++) {
            //    formData.append('question');
            //}
                               //The following getAll() function will return both username values in an array:

            data=formData.getAll('question'); // Returns ["Chris", "Bob"]
            console.log(data);
        });
*/