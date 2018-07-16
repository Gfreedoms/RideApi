
function toggle_element(id){
	var element = document.getElementById(id);
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

function show_element(id){
	var element = document.getElementById(id);
	element.style.display = "block";

}

function hide_element(id){
	var element = document.getElementById(id);
	element.style.display = "none";
}

function initialise(){
	show_element("search_resuts");
	hide_element("post_offer_div");
	// hide all error inputs

}

function show_post_form(){
	show_element("post_offer_div");
	hide_element("search_resuts");
}

