var scroller = document.querySelector('#scroller');
var template = document.querySelector('#post_template');

//var loaded= document.querySelector('#loaded');
var sentinel = document.querySelector('#sentinel');
var counter = 0;

function load_items() {
    fetch(`/exam_slot_load?c=${counter}`).then((response) => {
        response.json().then((exam_slot) => {
            if (!exam_slot.length) {
                sentinel.innerHTML = 'No more Schedule';
            }
            for (var i = 0; i < exam_slot.length; i++) {
                let template_clone = template.content.cloneNode(true);
                template_clone.querySelector('#exam_title').innerHTML = `${exam_slot[i].exam_title}`;
                template_clone.querySelector('#exam_course').innerHTML = `${exam_slot[i].exam_course}`;
                template_clone.querySelector('#exam_date').innerHTML = `${exam_slot[i].exam_date}`;
                template_clone.querySelector('#exam_start_time').innerHTML = `${exam_slot[i].exam_start_time}`;
                template_clone.querySelector('#exam_end_time').innerHTML = `${exam_slot[i].exam_end_time}`;
                scroller.appendChild(template_clone);
                counter += 1;
                //loaded.innerHTML=`$(counter) items loaded`;
            }
        })
    })
}

var intersectionObserver = new IntersectionObserver(entries => {

    if (entries[0].intersectionRatio <= 0) {
        return;
    }
    load_items();

});
intersectionObserver.observe(sentinel);