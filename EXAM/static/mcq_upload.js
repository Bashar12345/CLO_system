


$(document).ready(function(){
    load();
});

function load(){
     //alert("Is it working");
    $("#total").focus();
    $("#totalbtn").click(function(){
        var total_questions= $("#total").val();
        var options = $("#option_total").val();
        alert(""+  total_questions);



        if (total_questions>0){
            createTable(total_questions);
        }


function createTable(total_questions){
    let inputTable='';

    inputTable='<table class="d-flex">'+
    ' <tr>'+
    '   <legend class="custom-control-label">Total how many Questions</legend>'+
    '   <input id="total" type="number" min="0" class="custom-select-md" name="numbers_of_questioned" required>'+

    ' <button class="btn btn-outline-primary" id="totalbtn" type="button"> <img src="{{url_for("static",filename="img/plus.png")}}" alt="Total" width="30px" height="25px" /> </button>'+
    '</tr>' ;

    for(i=0;i<total_questions;i++)
    {   
        createTable+= '<label for="question'+ i +'>MCQ Question '+ (i+1) +'}} :</label>'
'<input class="col" type="text" id="question'+ i +' " name="question '+ i +'" placeholder="Enter Question-'+ (i+1)+' "/>'+
        '<br/>'+
        '<div class="form-group custom-select">';

    for(j=0;i<options;j++)
    { 
    createTable+='<label for="options">Option-'+j+':</label>'+
            '<input id="options" name="op'+j+'"placeholder="Enter Option-'+j+'"/>'+
            '<br/>';

    }  
    createTable+='</div>'
        '<div class="form-group">'+
        '<label for="answer">MCQ Answer {{ i + 1 }} :</label>'+
        '<input class="col" type="text" id="answer" name="answer" placeholder="Enter Answer-'+ (i+1) +'"/>'+
        '<br/>'+
    '</div>'+
    '</div>';

}

}
    });
}