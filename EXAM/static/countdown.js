//const countDownDate = new Date(date+start_time).getTime();
//const date_of_exam = document.getElementById("date").getAttribute("value");
//const starting_time = document.getElementById("time").getAttribute("value");
const exam_time = document.getElementById("exam_date").getAttribute("value");

console.log(typeof exam_time)
//document.getElementById("demo").innerHTML = date_of_exam;
//document.getElementById("demo1").innerHTML = starting_time;
//const countDownDate = new Date("Jan 19, 2021 17:40:25").getTime();
//const countDownDate = new Date(date_of_exam + " " + starting_time).getTime();
let countDownDate;
if (exam_time != null) {
    countDownDate = new Date(exam_time + "").getTime();
} else {
    const date_of_exam = document.getElementById("date").getAttribute("value");
    const starting_time = document.getElementById("time").getAttribute("value");
    countDownDate = new Date(date_of_exam + " " + starting_time).getTime();
}

// Update the count down every 1 second
const x = setInterval(function () {
    // Get today's date and time
    const now = new Date().getTime();

    // Find the distance between now and the count down date
    const distance = countDownDate - now;

    // Time calculations for days, hours, minutes and seconds
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result in the element with id="show_realtime"
    document.getElementById("show_realtime").innerHTML =
        days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

    // If the count down is finished, write some text
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("show_realtime").innerHTML =
            "Exam Started, So go to backepage and retry to join the exam ";
        document.getElementById("submit_answer").submit();
    }
}, 1000);
