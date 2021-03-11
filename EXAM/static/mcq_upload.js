$(document).ready(function () {
    load();
});

function load() {
    //alert("Is it working");
    $("#total").focus();
    $("#options").focus();
    $("#course_title").focus();
    $("#course_code").focus();


    $("#course_title").change(function(){
        var course = $("#course_title").val();
        var code =$("#course_code");
        //alert("" + course);
            fetch(`/mcqUpload_select_load?c=${course.replace(/\s+/g, ';')}`).then(function(response){
                response.json().then(function(route_data){
                    var optionHTML='';
                    for (var i = 0; i < route_data.length; i++) {
                        optionHTML+=`<option value="${route_data[i].course_code}">${route_data[i].course_code}</option>`;
                        //console.log(optionHTML)
        
                    }
                    code.append(optionHTML);
                });

    });
});

$("#course_code").change(function(){
    var code =$("#course_code");
    var lessons =$('#lesson');
    

});

    $("#total_btn").click(function(){
        var total_questions = $("#total").val();
        var options = $("#options").val();
        //alert("" + total_questions);

        if (total_questions > 0) {
            createTable(total_questions,options);
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

    });
}









        function createTable(total_questions,options) {
            var inputTable="";
            var count =1;
            inputTable =`<div class="container">`;

for (let i = 0; i < total_questions; i++) {
    inputTable += `  <div>
    <label class="form-control-label" for="question-${i + 1}">
    <h4>Question ${i + 1}:</h4>
    </label>
</div>
<div>
<input class="form-control" id="question-'+ i +'" name="question" type="text"
    placeholder="EnterQuestion-${i + 1}" /><br/>
</div>`;
inputTable += `<label class="form-control-label" >MCQ-${i + 1} Answer:</label><br/>`;
    inputTable += `<input class="form-control-lg" type="text" id="answer" name="answer${i}" 
        placeholder="Enter Answer-${i + 1}"><br/>`;

        inputTable +=  `<div class="row">`;
for (let j = 0; j < options; j++) {
    
    inputTable +=`<label>Option-${j+1}:</label><br>`;

    inputTable +=`<input type="text" id="options" name="op[${j+count}]" placeholder="Enter Option-${j+1}"><br/>`;
    if(j==1){
        inputTable += `<div class="w-100"></div>`;
    } 
        count++;
    
} 
        inputTable += `</div>`;

$('#addQuestion').append(inputTable);

        }
    }  

