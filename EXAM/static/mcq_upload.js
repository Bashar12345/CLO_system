$(document).ready(function () {
    load();
});

function load() {
    //alert("Is it working");
    $("#total").focus();
    $("#options").focus();

    $("#total_btn").click(function () {
        var total_questions = $("#total").val();
        var options = $("#options").val();
        //alert("" + total_questions);

        if (total_questions > 0) {
            createTable(total_questions,options);
        }

    $('#add').click(function(){
     var formData = new FormData();
           // for (let i = 0; i < total_questions; i++) {
            //    formData.append('question');
            //}
                               //The following getAll() function will return both username values in an array:

            data=formData.getAll('question'); // Returns ["Chris", "Bob"]
            console.log(data);
        });


    });
}

        function createTable(total_questions,options) {
            var inputTable="";

            inputTable = '<div class="input-group">' ;

            for (let i = 0; i < total_questions; i++) {
 inputTable += ' <label class="form-group" for="question'+ i +'">MCQ Question ' + (i + 1) +':</label>'+
 '<input class="custom-control-input-lg" type="text" id="question-'+ i +'" name="question'+ i +'" placeholder="Enter Question-'+(i+1)+'"/>  ';

                for (let j = 0; j < options; j++) {
      inputTable += ` <br/><label for="options">Option-${j+1}:</label><br/> <input id="options" name="op[${j+1}]" placeholder="Enter Option-${j+1}"/></br>  `;
                }
    inputTable += ` <label for="answer">MCQ Answer${i + 1}:</label><br/><input type="text" id="answer" name="answer${i}" placeholder="Enter Answer-${i + 1} "/> <br/> `;

}
           inputTable += '</div>';
$('#addQuestion').append(inputTable);

        }


        

