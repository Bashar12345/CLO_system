var selected_title=document.getElementById("course_title");
var selected_code= document.getElementById('course_code');
var selected_lesson=document.getElementById('lesson');

selected_title.onchange=function(){
    var course_title=selected_title.getAttribute("value");
   // $(this).find(':selected').data('id');
    alert(""+course_title);

    fetch('/mcqUpload/'+course_title).then(function(response){
        response.json().then(function(route_data){
            var optionHTML='';
            for (var op in route_data.selected_code){
                optionHTML+=`<option ${op.course_code}>${op.course_code}</option>`;

            }
            selected_code.innerHTML=optionHTML;
        });
    });

}