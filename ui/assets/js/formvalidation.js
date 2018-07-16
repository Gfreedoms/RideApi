// values
// global variables
var uname;
var email;
var password;
var confirm_password;

var name_error;
var email_error;
var password_error;
var password_error2;

// index page form elements
var from_input;
var to_input;
var date_input;
var time_input;
var spots;
var description;

var from_error;
var to_error;
var date_error;
var time_error;
var spots_error;
var description_error;


// to initialize index validations
function initialise_index_validations(){
	// initilize form elements
	from_input=document.getElementById("from");
	to_input=document.getElementById("to");
	date_input=document.getElementById("date");
	time_input=document.getElementById("time");
	spots=document.getElementById("spots");
	description=document.getElementById("description");

	// add events

	from_input.addEventListener("blur",fromValidator,true);
	to_input.addEventListener("blur",toValidator,true);
	date_input.addEventListener("blur",dateValidator,true);
	time_input.addEventListener("blur",timeValidator,true);
	spots.addEventListener("blur",spotsValidator,true);
	description.addEventListener("blur",descriptionValidator,true);

	// initialize error elements
	from_error=document.getElementById("from_error");
	to_error=document.getElementById("to_error");
	date_error=document.getElementById("date_error");
	time_error=document.getElementById("time_error");
	spots_error=document.getElementById("spots_error");
	description_error=document.getElementById("description_error");
}

function validate_ride_post(){
	if(from_input.value==""){
		from_input.style.border="1px solid #d63031";
		from_error.style.visibility="visible";
		from_error.textContent="* from of the ride is required";
		from_input.focus()
		return false;
	}

	if(to_input.value==""){
		to_input.style.border="1px solid #d63031";
		to_error.style.visibility="visible";
		to_error.textContent="* destination is required";
		to_input.focus()
		return false;
	}

	if(date_input.value==""){
		date_input.style.border="1px solid #d63031";
		date_error.style.visibility="visible";
		date_error.textContent="* depature date is required";
		date_input.focus()
		return false;
	}


	if(time_input.value==""){
		time_input.style.border="1px solid #d63031";
		time_error.style.visibility="visible";
		time_error.textContent="* depature time is required";
		time_input.focus()
		return false;
	}

	if(spots.value==""){
		spots.style.border="1px solid #d63031";
		spots_error.style.visibility="visible";
		spots_error.textContent="* no of free seats is required";
		spots.focus()
		return false;
	}

	if(description.value==""){
		description.style.border="1px solid #d63031";
		description_error.style.visibility="visible";
		description_error.textContent="* description is required";
		description.focus()
		return false;
	}

}


// to initialize login form validation elements
function initialize_login_validation_elements(){
	email=document.getElementById("email");
	password=document.getElementById("password");

	//add blur event 
	email.addEventListener("blur",emailValidator,true);
	password.addEventListener("blur",passwordValidator,true);

	email_error=document.getElementById("email_error");
	password_error=document.getElementById("password_error");
}

//to initiallize sign up page elements
function initialise_signup_validation_elements(){
	uname=document.getElementById("name");
	email=document.getElementById("email");
	password=document.getElementById("password");
	confirm_password=document.getElementById("confirm_password");
 	//add blur events
	uname.addEventListener("blur",nameValidator,true);
	email.addEventListener("blur",emailValidator,true);
	password.addEventListener("blur",passwordValidator,true);
	confirm_password.addEventListener("blur",confirmValidator,true);

		// error display objects
	name_error=document.getElementById("name_error");
	email_error=document.getElementById("email_error");
	password_error=document.getElementById("password_error");
	password_error2=document.getElementById("password_error2");

	// name_error.style.visibility="hidden";
	// email_error.style.visibility="hidden";
	// password_error.style.visibility="hidden";
	// password_error2.style.visibility="hidden";
}

// to validate login inputs 
function validate_login(){
	var reg=/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

	if(email.value==""){
		email.style.border="1px solid #d63031";
		email_error.style.visibility="visible";
		email_error.textContent="* email is required";
		email.focus()
		return false;
		
	}else if(!reg.test(email.value)){
		email.style.border="1px solid #d63031";
		email_error.style.visibility="visible";
		email_error.textContent="* invalid email format";
		email.focus()
		return false;
	}

	if(password.value==""){
		password.style.border="1px solid #d63031";
		password_error.style.visibility="visible";
		password_error.textContent="* password is required";
		password.focus()
		return false;
	}
}

// to validate signup inputs
function validate_signup(){
	
	if(uname.value==""){
		uname.style.border="1px solid #d63031";
		name_error.style.visibility="visible";
		name_error.textContent="* name is required";
		uname.focus()
		return false;
	}

	var reg=/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

	if(email.value==""){
		email.style.border="1px solid #d63031";
		email_error.style.visibility="visible";
		email_error.textContent="* email is required";
		email.focus()
		return false;
		
	}else if(!reg.test(email.value)){
		email.style.border="1px solid #d63031";
		email_error.style.visibility="visible";
		email_error.textContent="* invalid email format";
		email.focus()
		return false;
	}

	if(password.value==""){
		password.style.border="1px solid #d63031";
		password_error.style.visibility="visible";
		password_error.textContent="* password is required";
		password.focus()
		return false;
	}else if(password.value.length<5){
		password.style.border="1px solid #d63031";
		password_error.style.visibility="visible";
		password_error.textContent="* weak password use at least 5 letters ";
		password.focus()
		return false;
	}

	if(password.value !=confirm_password.value ){
		password.style.border="1px solid #d63031";
		confirm_password.style.border="1px solid #d63031";
		password_error2.style.visibility="visible";
		password_error2.textContent="** password mismatch";
		confirm_password.focus()
		return false;
	}

}

// called on blur to check if name field has been filled such that errors styles 
// can be removed
function nameValidator(){
	if(uname.value!=""){
		uname.style.border="1px solid #d1d5da";
		name_error.innerHtml=""
		name_error.style.visibility="hidden";
		return true;
	}
}

// called on blur to check if email field has been filled such that errors styles 
// can be removed
function emailValidator(){
	if(email.value!=""){
		email.style.border="1px solid #d1d5da";
		email_error.innerHtml=""
		email_error.style.visibility="hidden";
		
		return true;
	}
}

// called on blur to check if password field has been filled such that errors styles 
// can be removed
function passwordValidator(){
	if(password.value!=""){
		password.style.border="1px solid #d1d5da"
		password_error.innerHtml=""
		password_error.style.visibility="hidden";
		
		return true;
	}
}

// called on blur to check if confirm password field has been filled such that errors styles 
// can be removed
function confirmValidator(){
	if(confirm_password.value!=""){
		password.style.border="1px solid #d1d5da"
		confirm_password.style.border="1px solid #d1d5da"
		password_error2.innerHtml=""
		password_error2.style.visibility="hidden";
		
		return true;
	}
}

// called on blur to check if from field has been filled such that errors styles 
// can be removed
function fromValidator(){
	if(from_input.value!=""){
		from_input.style.border="1px solid #d1d5da"
		from_error.innerHtml=""
		from_error.style.visibility="hidden";
		
		return true;
	}
}

// called on blur to check if to field has been filled such that errors styles 
// can be removed
function toValidator(){
	if(to_input.value!=""){
		to_input.style.border="1px solid #d1d5da"
		to_error.innerHtml=""
		to_error.style.visibility="hidden";
		
		return true;
	}
}

// called on blur to check if date field has been filled such that errors styles 
// can be removed
function dateValidator(){
	if(date_input.value!=""){
		date_input.style.border="1px solid #d1d5da"
		date_error.innerHtml=""
		date_error.style.visibility="hidden";
		
		return true;
	}
} 

// called on blur to check if time field has been filled such that errors styles 
// can be removed
function timeValidator(){
	if(time_input.value!=""){
		time_input.style.border="1px solid #d1d5da"
		time_error.innerHtml=""
		time_error.style.visibility="hidden";
		
		return true;
	}
} 

// called on blur to check if spots field has been filled such that errors styles 
// can be removed
function spotsValidator(){
	if(spots.value!=""){
		spots.style.border="1px solid #d1d5da"
		spots_error.innerHtml=""
		spots_error.style.visibility="hidden";
		
		return true;
	}
} 

// called on blur to check if description field has been filled such that errors styles 
// can be removed
function descriptionValidator(){
	if(description.value!=""){
		description.style.border="1px solid #d1d5da"
		description_error.innerHtml=""
		description_error.style.visibility="hidden";
		
		return true;
	}
}
