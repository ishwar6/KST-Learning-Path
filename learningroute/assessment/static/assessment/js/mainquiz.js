var firsttime=0;


window.addEventListener("blur", function(event) { 
  var valcheck=Number($('input[name="validity"]').val());

  firsttime=firsttime+1;
valcheck=valcheck-1;

$('input[name="validity"]').val(valcheck);

$('input[name="validity2"]').val(valcheck);
  if(firsttime>=2 || valcheck<1)
  {
    
    $('input[name="validity"]').val("0");
     $('input[name="validity2"]').val("0");
     $("#submitter").click();
  }

alert("[WARNING] You need to remain active only in the current test window, If you try to open a new tab or window again, you will be disqualified");}, false);
window.addEventListener("focus", function(event) { 
}, false);

// "Main method" which will create all the objects and render the Quiz.
$(document).ready(function() {
  // Create an instance of the Quiz object
 // var quiz = new Quiz('My Quiz');


  $("#validity").hide();
   $("#timeshow").hide();
   $("#disableforpropertime").hide();

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);
        if(minutes==0 && seconds==0)
          $("#endgame").click();
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.text(minutes + ":" + seconds);
        $('input[name="timeshow"]').val(minutes + ":" + seconds);
        $('input[name="timeshow_second"]').val(minutes + ":" + seconds);
          $("#disableforpropertime").show();
        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}

    temp=$( "#time" ).text();
    var fields = temp.split(':');
    $('input[name="timeshow"]').val(Number(fields[0]) + ":" + Number(fields[1])-1);
        $('input[name="timeshow_second"]').val(Number(fields[0]) + ":" + Number(fields[1])-1);
    var fiveMinutes = 60 * Number(fields[0])+Number(fields[1])-1,
        display = $('#time');
    startTimer(fiveMinutes, display);




  // Create Question objects from all_questions and add them to the Quiz object
  //for (var i = 0; i < all_questions.length; i++) {
    // Create a new Question object
   // var question = new Question(all_questions[i].question_string, all_questions[i].choices.correct, all_questions[i].choices.wrong);
    
    // Add the question to the instance of the Quiz object that we created previously
   // quiz.add_question(question);
  ///}
  
  // Render the quiz
 // var quiz_container = $('#quiz');
//  quiz.render(quiz_container);

});