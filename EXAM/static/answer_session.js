
       $(document).ready(function () {
              load();
       });

       function load() {
              $('#add_data').focus();
              $('#btn_next_question').focus();
              $('#question_card').focus();
              var next_count = 1;
              var parse = 0;


              var questions = JSON.parse('{{question_mcq_for_current_session | tojson}}');
              //console.log(questions);
              var viewQuestion = '';
              var question_block = $('#add_data');


              viewQuestion += ` <div id='question_card' class="card-block">`;
              // for (var i = 0; i < questions.length ; i++) {
              for (var i = 0; i < 1; i++) {

                     for (var j in questions[i]) {
                            viewQuestion += `  <div class="card-header h5">
                            
                                   <div class="card-title text-primary">
                                           <b>${j}</b> 
                                   </div>
                       

                            </div>`;


                            viewQuestion += ` <div class="card-body">`;
                            for (var k in questions[i][j]) {
                                   viewQuestion += ` <div class="card-text text-secondary">
<input id = "chk ${questions[i][j][k]}" aria - label="Checkbox for following text input" type = "radio"
              value = " ${questions[i][j][k]}" name = "selected_option" />
              
              <label for="chk ${questions[i][j][k]}">option ${k} : ${questions[i][j][k]}</label>
                                   </div> `;

                            }
                            viewQuestion += ` </div>`;
                     }


              }
              viewQuestion += ` </div>`;
              question_block.append(viewQuestion);




              $('#btn_next_question').click(function () {
                     $('#question_card').empty();
                     $('#add_data').empty();

                     //$('#count').html(next_count);
                     viewQuestion += `<br> <div id='question_card' class="card-body">`;
                     for (var i = 0; i < 1; i++) {


                            for (var j in questions[next_count]) {
                                   viewQuestion += `  <div class="card-header h5">
                                   <div class="card-title text-primary">
                                           <b>${j}</b> 
                                   </div> </div>`;


                                   viewQuestion += ` <div class="card-body">`;

                                   for (var k in questions[next_count][j]) {
                                          viewQuestion += ` <div class="card-text text-secondary">
<input id = "chk ${questions[next_count][j][k]}" aria - label="Checkbox for following text input" type = "radio"
              value = " ${questions[next_count][j][k]}" name = "selected_option" />
              
              <label for="chk ${questions[next_count][j][k]}">option ${k} : ${questions[next_count][j][k]}</label>
                                   </div> `;

                                   }
                                   viewQuestion += ` </div>`;
                            }


                     }

                     viewQuestion += ` </div>`;
                     question_block.append(viewQuestion);
                     next_count += 1;
                     //console.log(next_count)

                     if (next_count == questions.length) {
                            $('#btn_next_question').html('No more Questions')
                     }



              })






       }