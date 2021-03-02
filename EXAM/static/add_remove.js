

    $(document).ready(function () {
        let max_fields = 10;
        let add_input = $('.add-input');
        let input_wrapper = $('.input-wrapper')
        let new_input = '<div><input type="text" id="lesson_name" name="total_lesson[]"  value=""><a href="javascript:void(0);" class="remove-input" title="remove input"><img src="/static/img/minus.png" type="button" class="btn-outline-light"></a></div> '
        let add_count = 1;
        $(add_input).click(function () {
            if (add_count < max_fields) {
                add_count++;
                $(input_wrapper).append(new_input);
            }
        });
        $(input_wrapper).on('click','.remove-input',function (e){
            e.preventDefault();
            $(this).parent('div').remove();
             add_count--;
        });
    });































//  const formData = new FormData();
// const total_lessons = formData.get('total_lesson')
/*  var lessons = document.getElementById("total_lessons").value;
  //alert(total_lessons)
  console.log(typeof (lessons))
  var total_lessons = parseInt(lessons)
  console.log(typeof (total_lessons))

  const URL = '/create_course'
  const xhr = new XMLHttpRequest();
  sender = JSON.stringify(total_lessons)
  xhr.open('POST', URL);
  xhr.send(sender)*/

/* // Create a form synamically
 var form = document.createElement("form");
 form.setAttribute("method", "post");
 var br = document.createElement("br");

 // Create an input element for  Lesson_Name
 for (let i = 0; i < total_lessons; i++) {
     console.log(typeof (total_lessons))
     const lessonName = document.createElement("input");
     lessonName.setAttribute("type", "input");
     lessonName.setAttribute("class", "col-4");
     lessonName.setAttribute("onchange", "GetEntered()")//change kore look back
     lessonName.setAttribute("name", "lesson_name" + i);
     lessonName.setAttribute("id", "lesson_name" + i);
     lessonName.setAttribute("placeholder", "Lesson_name" + i);
     form.appendChild(br.cloneNode())
     form.appendChild(lessonName);
     document.getElementsByTagName("input")[0]
         .appendChild(form);
 }*/