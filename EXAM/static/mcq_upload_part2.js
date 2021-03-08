var scroller = document.querySelector("#scroller");
var template = document.querySelector("#post_template");
var legend = document.querySelector("#legend");
const user_type = document.getElementById("user_type").getAttribute("value");
//var loaded= document.querySelector('#loaded');
var sentinel = document.querySelector("#sentinel");
var counter = 0;

function load_items() {
    fetch(`/mcqUpload_lesson_load?c=${counter}=${user_type}`).then((response) => {
        response.json().then((course_slot) => {
            if (!course_slot.length) {
                sentinel.innerHTML = "No more Courses";
            }
            for (var i = 0; i < course_slot.length; i++) {
                let template_clone = template.content.cloneNode(true);
                template_clone.querySelector("#link").href = `/question_view/${course_slot[i].course_code}`;
                template_clone.querySelector("#course_title").innerHTML = `${course_slot[i].course_title}`;
                template_clone.querySelector("#course_code").innerHTML = `${course_slot[i].course_code}`;
                template_clone.querySelector("#course_caption").innerHTML = `${course_slot[i].course_caption}`;
                template_clone.querySelector("#course_duration").innerHTML = `${course_slot[i].course_duration}`;
                scroller.appendChild(template_clone);
                counter += 1;
                //loaded.innerHTML=`$(counter) items loaded`;
            }
        });
    });
}