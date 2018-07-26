function create_cookie(name,value,days){
  var expires;
  if(days){
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000))
    expires = date.toGMTString();
  }else{
    expires="";
  }

  document.cookie = name+"="+value+";expires="+expires+";path=/";
}


function get_cookie(name){
  var name_eq = name+"=";
  var decode_cookie = decodeURIComponent(document.cookie);
  var all_cookies=decode_cookie.split(';');

  for(var i=0;i < all_cookies.length;i++) {
      var cookie = all_cookies[i];
      while (cookie.charAt(0) === ' ') {
        cookie = cookie.substring(1,cookie.length);
      }

      if (cookie.indexOf(name_eq) === 0) {
        return cookie.substring(name_eq.length,cookie.length);
      }
  }
  return null;

}

function show_user(){
  name=get_cookie("users_name");
  document.getElementById("logged_user").innerHTML=name;
  auth_token=get_cookie("auth_token");
    if(auth_token=="" || auth_token==" "){
      window.location.href = "login.html";
    }
}

function log_out(){
   create_cookie("auth_token","",1);
   create_cookie("users_name","",1);

   show_user();
}
