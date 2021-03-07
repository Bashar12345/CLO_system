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

            inputTable =` <section class="container">
            <form>
                <fieldset class="btn block btn-outline-light">`;
                    

for (let i = 0; i < total_questions; i++) {
    inputTable += `<div>
 <label class="form-control-label" for="question-${i + 1}">
     <h4>Question ${i + 1}:</h4>
 </label>
</div>

<div>
 <input class="form-control" id="question-'+ i +'" name="question" type="text"
     placeholder="EnterQuestion-${i + 1}" /><br />
</div>


<div class="row">`;

for (let j = 0; j < options; j++) {

    inputTable += `<div class="col"><label for="options">Option-${j+1}:</label><br />
                            <input class="form-control" type="text" id="options" name="op[${j+count}]"
                                placeholder="Enter Option-${j+1}" />
                        </div> `;
                        if(j==1){
                            inputTable += ` <div class="w-100"></div>`;
                        }
                }
                count++;
    inputTable += `<br />
    <div>
        <label for="answer">MCQ-${i + 1} Answer:</label>
    </div>
    <div>
        <input class="form-control" type="text" id="answer" name="answer${i}" 
        placeholder="Enter Answer-${i + 1}" />
    </div>`;

}
        inputTable += `</fieldset></form></section>`;

$('#addQuestion').append(inputTable);

        }


        

