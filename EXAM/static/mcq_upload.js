$(document).ready(function () {
    load();
});

function load() {
    //alert("Is it working");
    $("#total").focus();
    $("#options").focus();
    //$("#btn_course_title").focus();
    $("#btn_course_code").focus();
    $("#btn_option").focus();
    $("#link_course_code").focus();

    $("#btn_course_code").click(function(){
        $('#lesson').empty();
        var code =$("#course_code").val();
        var lessons =$('#lesson');
        $('#clo').empty();
        var clos =$('#clo');
    
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
    fetch(`/mcqUpload_clo_selection_load?c=${code}`).then(function(response){
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

// $("#btn_course_code").click(function(){
//     $('#clo').empty();
//     var code =$("#course_code").val();
//     var clos =$('#clo');



// });

        var count=1
        var op_count =5 
        var op_ans_count=5
        var  question_count =0

    $("#total_questions_btn").click(function(){
        var inputTable='';
        
        //$('#addQuestion').empty();    
        //alert("" + total_questions);
        //{#% if count.append(count.pop() + 1) %#}{#% endif %#} {# increment count by 1 #}

        
    inputTable += ` <label for="question${question_count+=1}">
    <h4>Question ${question_count} :</h4>
</label>
<input  class="form-control" type="text" id="question1" name="question${question_count}" placeholder="Enter Question-${question_count} "> 
<br/> <div class="form-group"> <br/>`;
    $('#q_counter').attr({"value":question_count})
    $('#q_counter').html(question_count)
// inputTable += `<input class="form-control" type="text" id="answer" name="answer${question_count}" placeholder="Enter Answer-${question_count}"><br/>`;

for(var i=0;i<6;i++){
    inputTable += `<label for="options">Option-${i+1}:</label> 
    <input class="form-control-sm" id="options" name="op[${op_count+=1}]" placeholder="Enter Option-1">`;
    }
    inputTable += `<br>
    <label for="answer${question_count}">
        <h4>Answer ${question_count} :</h4>
    </label><br>
    <select class="custom-select-md btn-outline-info"  name="answer${question_count}" type="text" placeholder="Enter Answer- ${question_count}" required><br/>`;
    for(var i=0;i<6;i++){
        inputTable += `<option type="text" value="op${op_ans_count+=1}">Option-${i+1}</option> `;
    }

    inputTable += `</select><br/>`;

    inputTable += `<br/></div>`;

    $('#addQuestion').append(inputTable);

    });

}





//     $("#btn_course_title").click(function(){
//         $('#course_code').empty();
//         var course = $("#course_title").val();
//         var code =$("#course_code");
//         var len =0
//         //var lessons =$('#lesson');
//         //alert("" + course);
//             fetch(`/mcqUpload_course_code_selection_load?c=${course.replace(/\s+/g, ';')}`).then(function(response){
//                 response.json().then(function(route_data){
//                     var option_code_HTML='';
//                     //var option_lesson_HTML='';
//                     option_code_HTML+=`<option value="null">Choose one</option>`;
                    
//                     for (var i = 0; i < route_data.length; i++) {
//                         option_code_HTML+=`<option value="${route_data[i].course_code}">${route_data[i].course_code}</option>`;
//                         //option_lesson_HTML+=`<option value="${route_data[i].course_lessons}">${route_data[i].course_lessons}</option>`;
//                         //console.log(optionHTML)
//                         //console.log(option_lesson_HTML)
                        
//                     }
//                     code.append(option_code_HTML);
//                     len++
//                     //lessons.append(option_lesson_HTML);

//                 });
//     });
// });



//     $("#total_questions_btn").click(function(){
//         //$('#addQuestion').empty();
//         var total_questions = $("#total").val();
//         var options = $("#options").val();
//         //alert("" + total_questions);
//         if (total_questions > 0) {
//             createTable(total_questions,options);
//         }
//     });

// }

//         function createTable(total_questions,options) {
//             var inputTable="";
//             var count =1;
//             inputTable =`<div class="container">`;

// //{#% if count.append(count.pop() + 1) %#}{#% endif %#} {# increment count by 1 #}

// for (var i = 0; i <total_questions; i++) {
//     inputTable += `  <div>
//     <label class="form-control-label" for="question-${i + 1}"><br/>
//     <h4>Question ${i + 1}:</h4>
//     </label>
// </div>
// <div>
// <input class="form-control" id="question-'+ i +'" name="question${i}" type="text"
//     placeholder="EnterQuestion-${i + 1}" /><br/>
// </div>`;
// inputTable += `<label class="form-control-label" ><h5>MCQ-${i + 1} Answer:</h5></label><br/>`;
//     inputTable += `<input class="form-control" type="text" id="answer" name="answer${i}" 
//         placeholder="Enter Answer-${i + 1}">`;

//         inputTable +=  `<div class="row"><br/>`;
// for (var j = 0; j < options; j++) {
    
//     inputTable +=`<div class="input-group mb-3"><label>Option-${j+1}:</label><br>
//     <div class="input-group-append mb-3"><input type="text" name="op[${j+count}]" placeholder="Enter Option-${j+1}"></div><br/>`;
    
//     inputTable += `</div>`;
// } 
//         inputTable += `</div>`;
//         count=count+parseInt(options);
//         }

//         $('#addQuestion').append(inputTable);
//     }  




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