function GetSelected() {
    //Create an Array.
    var selected = [];
    const data = ['🦊', '🐮'];
    //var enrollForm = document.forms["enrolForm"]; 
    //var enroll_key =  

    //Reference the Table.
    var tblStudents = document.getElementById("tblStudents[1]");

    //Reference all the CheckBoxes in Table.
    var chbks = tblStudents.getElementsByTagName("INPUT");

    // Loop and push the checked CheckBox value in Array.
    for (var i = 0; i < chbks.length; i++) {
        if (chbks[i].checked) {
            selected.push(chbks[i].value);
            data.splice(
                data.length,
                0, chbks[i].value);
        }
    }

    //Display the selected CheckBox values.
    if (selected.length > 0) {
        //+ selected.join(",")
        console.log(data); // ['🦊', '🐮', '🐧', '🐦', '🐤']
        console.log(selected);
        var URL = '/students_load'
        var xhr = new XMLHttpRequest();
        var sender = JSON.stringify(selected)
        xhr.open('POST', URL);
        xhr.send(sender)
        //xhr.abort()
        //alert("A Joining Key has been sending to the student, by the system ");
    }
    //document.querySelector('arraySelected').value=selected.toString()


}