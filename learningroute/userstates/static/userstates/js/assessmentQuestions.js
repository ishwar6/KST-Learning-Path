let formType = -1;

function submitForm(){
    if(formType === 1){
        if(document.querySelector('#integerType').value.length > 0){
            document.querySelector(".submit-button").type = "submit";
            document.querySelector(".submit-button").click();
        }
    }
    if(formType === 2){
        if(document.querySelector('#singleChoiceInput').value >= 1 && document.querySelector('#singleChoiceInput').value  <= 4){
            document.querySelector(".submit-button").type = "submit";
            document.querySelector(".submit-button").click();
        }
    }
    if(formType === 3){
        if(document.querySelector('#InputMultiple1').value == 1 || document.querySelector('#InputMultiple2').value == 1 
        || document.querySelector('#InputMultiple3').value == 1 || document.querySelector('#InputMultiple4').value == 1
        ){
            document.querySelector(".submit-button").type = "submit";
            document.querySelector(".submit-button").click();
        }
    }

}
if(document.querySelector("#integerType")){
document.querySelector("#integerType").addEventListener("input", () => {
    formType =1;
    if(document.querySelector("#integerType").value.length > 0){
        document.querySelector(".submit-button").classList.add("submit-buttonActive")
    }else{
        document.querySelector(".submit-button").classList.remove("submit-buttonActive")
    }
})}


function singleChoice(button, value){
    document.querySelector("input-singleChoice").querySelectorAll("button").forEach(button => button.classList.remove("buttonInput-active"));
    button.classList.add("buttonInput-active");
    document.querySelector('#singleChoiceInput').value = value;
    document.querySelector(".submit-button").classList.add("submit-buttonActive")
}
function multipleChoice(button, value){
    if(button.classList.contains("buttonInput-active")){
        button.classList.remove("buttonInput-active")
        document.querySelector(value).value = 0
    }else{
        button.classList.add("buttonInput-active")
        document.querySelector(value).value = 1
    }
    if(document.querySelector('#InputMultiple1').value == 1 || document.querySelector('#InputMultiple2').value == 1 
    || document.querySelector('#InputMultiple3').value == 1 || document.querySelector('#InputMultiple4').value == 1){
        document.querySelector(".submit-button").classList.add("submit-buttonActive")
    }else{
        
        document.querySelector(".submit-button").classList.remove("submit-buttonActive")
        }
    
}
function addInputs(responseData){
    if(responseData.input_type){
        formType =1;
        document.querySelector(".normalForm-input").innerHTML = `
        <div class="input-text">
        <label for="integerType">Enter your answer</label>
        <input type="number" name="integertype" id="integerType">
      </div> 
        `
    }
    if(responseData.singleOption){
        formType =2;
        document.querySelector(".normalForm-input").innerHTML = `
        <div class="input-singleChoice">
        <input type="text" id="singleChoiceInput" name="rad">
        <button type="button" onclick="singleChoice(this,1)" >${responseData.option1}</button>
        <button type="button" onclick="singleChoice(this,2)" >${responseData.option2}</button>
        <button type="button" onclick="singleChoice(this,3)" >${responseData.option3}</button>
        <button type="button" onclick="singleChoice(this,4)" >${responseData.option4}</button>
      </div>
        `
    }
    if(!responseData.input_type && !responseData.singleOption){
        formType =3;
        document.querySelector(".normalForm-input").innerHTML = `
        <div class="input-multipleChoice">
        <input type="text" id="singleChoiceInput" name="rad">
        <button type="button" onclick="multipleChoice(this,'1InputMultiple')" >${responseData.option1}</button>
        <button type="button" onclick="multipleChoice(this,'2InputMultiple')" >${responseData.option2}</button>
        <button type="button" onclick="multipleChoice(this,'3InputMultiple')" >${responseData.option3}</button>
        <button type="button" onclick="multipleChoice(this,'4InputMultiple')" >${responseData.option4}</button>
      </div>
        `
    }
    document.querySelector(".assessmentQuestions-content").innerHTML = `
    <h3>${responseData.id}</h3>
      <p>${responseData.text} </p>
      ${responseData.question_image.length > 0 && 
    
        '<img id ="image-question" src="${responseData.question_image}" height="250px" width="250px">'
    }
    `
}


$(document).ready(function(){
            var myform = $('.normalForm')
            myform.on("submit", function(e){
                e.preventDefault()
                var formdata = $(this).serialize()
                console.log(formdata)

            let $thisURL = myform.attr('data-url') 
            $.ajax({
            method: "POST",
            url: $thisURL,
            data: formdata,
            success: handleFormSuccess,
            error: handleFormError,
            })
            })

            let responseData = null;
            function handleFormSuccess(data, textStatus, jqXHR){
                if(data.empty){
                    window.location.href = '/userstates/report/';
                }
                
                responseData = data.question_image[0];
                console.log(responseData,data)
                console.log(responseData)
                if(responseData != null && Object.keys(responseData).length !== 0){
                    addInputs(responseData)
                    document.querySelector(".submit-button").classList.remove("submit-buttonActive")
                }
            }

        function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR)
        console.log(textStatus)
        console.log(errorThrown)
        }
})
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
var cookies = document.cookie.split(';');
for (var i = 0; i < cookies.length; i++) {
var cookie = jQuery.trim(cookies[i]);
// Does this cookie string begin with the name we want?
if (cookie.substring(0, name.length + 1) === (name + '=')) {
    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    break;
}
}
}
return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        }
});
