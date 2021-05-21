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
    $("#q_counter").focus();

    //$("#answer0").focus();

    $('#addQuestion').focus()
    //$("#options").focus();
    // for (q_count in $('#q_counter').attr('value')) {
    //     var q_count_string = "#" + "answer" + toString(q_count)
    //     console.log(q_count_string);
    //     $(q_count_string).focus();
    // }



    var check = $('#link_course_code').attr('value');
    //console.log(check)
    if (check != 'teacher') {
        var clos = $('#clo');
        var code = check;

        fetch(`/mcqUpload_clo_selection_load?c=${code}`).then(function (response) {
            response.json().then(function (clo_array) {
                var optionHTML = '';
                for (var i = 0; i < clo_array.length; i++) {
                    optionHTML += `<option value="${clo_array[i]}">${clo_array[i]}</option>`;
                    console.log(optionHTML);
                }
                clos.append(optionHTML);
            });
        });
    }


    $("#btn_course_code").click(function () {
        $('#lesson').empty();
        var code = $("#course_code").val();
        var lessons = $('#lesson');
        $('#clo').empty();
        var clos = $('#clo');

        fetch(`/mcqUpload_lesson_selection_load?c=${code}`).then(function (response) {
            response.json().then(function (lesson_array) {
                var optionHTML = '';
                for (var i = 0; i < lesson_array.length; i++) {
                    optionHTML += `<option value="${lesson_array[i]}">${lesson_array[i]}</option>`;
                    console.log(optionHTML);
                }
                lessons.append(optionHTML);
            });
        });
        fetch(`/mcqUpload_clo_selection_load?c=${code}`).then(function (response) {
            response.json().then(function (clo_array) {
                var optionHTML = '';
                for (var i = 0; i < clo_array.length; i++) {
                    optionHTML += `<option value="${clo_array[i]}">${clo_array[i]}</option>`;
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
    var q_counter = 0;
    console.log(q_counter)
    var count = 1
    var op_count = 5
    var op_ans_count = 5
    var question_count = 0
    var count = 1




    $("#total_questions_btn").click(function () {
        var inputTable = '';
        q_counter += 1;
        console.log(q_counter)
        //        $('#q_counter').attr('value') = q_counter;
        $('#q_counter').val(q_counter);


        inputTable += ` <label for="question${count+=1}">
    <h4>Question ${count} :</h4>
</label>
<input  class="form-control"
 type="text" 
 id="question1" 
 name="question${question_count+=1}" 
 placeholder="Enter Question-${count}  (Dont use fullstop in the question)"> 
<br/> 
<div class="form-group"> <br/>`;

        for (var i = 0; i < 6; i++) {
            inputTable += `
    <div class="form-group">
    <label for="options">Option- ${i+1}:</label> 
    <input class="form-control-sm" id="options" name="op[${op_count+=1}]" placeholder="Enter Option- ${i+1}">
    </div>`;
        }
        inputTable += `<br>
    <label for="answer${count}">
        <h4>Answer ${count} :</h4>
    </label><br>
    <select class="custom-select btn-outline-info"  
    name="answer${question_count}" 
    id="answer${question_count}"
    type="text" 
    placeholder="Enter Answer- ${count}" required><br/>`;

        for (var i = 0; i < 6; i++) {
            inputTable += `<option type="text" value="op${op_ans_count+=1}">Option-${i+1}</option> `;
        }

        inputTable += `</select><br/>`;

        inputTable += `<br/></div>`;

        $('#addQuestion').append(inputTable);

    });

    $("#answer0").focus();
    $("#answer1").focus();
    $("#answer2").focus();
    $("#answer3").focus();
    $("#answer4").focus();
    $("#answer5").focus();
    $("#answer6").focus();
    $("#answer7").focus();
    $("#answer8").focus();
    $("#answer9").focus();


    $("#answer0").change(function () {
        var op = $("#answer0").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer1").change(function () {
        var op = $("#answer01").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer2").change(function () {
        var op = $("#answer2").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer3").change(function () {
        var op = $("#answer3").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer4").change(function () {
        var op = $("#answer4").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer5").change(function () {
        var op = $("#answer5").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer6").change(function () {
        var op = $("#answer6").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer7").change(function () {
        var op = $("#answer7").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer8").change(function () {
        var op = $("#answer8").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });
    $("#answer9").change(function () {
        var op = $("#answer9").val();
        console.log(op);
        var op_id = "#" + op
        //console.log(op_id)
        var field_value = document.getElementById(op).value;
        console.log(field_value)
        if (!field_value) {
            alert("Option Should not Empty ");

        }

    });



}

//     $("#total_questions_btn").click(function(){
//         var inputTable='';
//         q_counter+=1;
//         console.log(q_counter)
//         $('#q_counter').attr('value')=q_counter;


//         //$('#addQuestion').empty();    
//         //alert("" + total_questions);
//         //{#% if count.append(count.pop() + 1) %#}{#% endif %#} {# increment count by 1 #}


//     inputTable += ` <label for="question${count+=1}">
//     <h4>Question ${count} :</h4>
// </label>
// <input  class="form-control" type="text" id="question1" name="question${question_count+=1}" placeholder="Enter Question-${count} "> 
// <br/> <div class="form-group"> <br/>`;
//     $('#q_counter').attr({"value":question_count})
//     $('#q_counter').html(question_count)
// // inputTable += `<input class="form-control" type="text" id="answer" name="answer${question_count}" placeholder="Enter Answer-${question_count}"><br/>`;

// for(var i=0;i<6;i++){
//     inputTable += `
//     <div class="form-group">
//     <label for="options">Option- ${i+1}:</label> 
//     <input class="form-control-sm" id="options" name="op[${op_count+=1}]" placeholder="Enter Option- ${i+1}">
//     </div>`;
//     }
//     inputTable += `<br>
//     <label for="answer${count}">
//         <h4>Answer ${count} :</h4>
//     </label><br>
//     <select class="custom-select-md btn-outline-info"  name="answer${question_count}" type="text" placeholder="Enter Answer- ${count}" required><br/>`;
//     for(var i=0;i<6;i++){
//         inputTable += `<option type="text" value="op${op_ans_count+=1}">Option-${i+1}</option> `;
//     }

//     inputTable += `</select><br/>`;

//     inputTable += `<br/></div>`;

//     $('#addQuestion').append(inputTable);

//     });





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