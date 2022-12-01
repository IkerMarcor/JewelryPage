$(document).ready(function() {
    $("#register").submit(function(e) {
      //---------------^---------------
      e.preventDefault();
      var firstname = $('#First_name').val(),
        lastname = $('#last_name').val(),
        username = $('#reg_username').val(),
        password = $('#password').val(),
        email = $('#email').val();
      $.ajax({
        type: "POST",
        url: "doRegister.php",
        data: "first_name=" + firstname + "&last_name=" + lastname + "&username=" + username + "&password=" + password + "&email=" + email,
        success: function(html) {
          console.log(html);
        }
      });
      return false;
  
    });
  });
  
function login() {
    let correo = document.getElementById("email").value;
    let contrasena = document.getElementById("contrasena").value;
    let informacion_login = [{'correo':correo},{'contrasena':contrasena}]

        $.ajax({
            type: "POST",
            url: "/login",
            data: JSON.stringify(informacion_login),
            contentType: "application/json",
            dataType: 'json',
            success: function(result) {
            console.log("Result:");
            console.log(result);
             }  
            });

    window.location.reload();
        }

function register(){
    let username = document.getElementById('username').value;
    let nombre = document.getElementById('nombre').value;
    let apellido1= document.getElementById('apellido1').value;
    let apellido2= document.getElementById('apellido2').value;
    let correo= document.getElementById('email').value;
    let contrasena1= document.getElementById('contrasena1').value;
    let contrasena2= document.getElementById('contrasena2').value;

    let informacion_registro = [{},{},{},{},{}];

        $.ajax({
            type: "POST",
            url: "/register",
            data: JSON.stringify(informacion_registro),
            contentType: "application/json",
            dataType: 'json',
            success: function(result) {
            console.log("Result:");
            console.log(result);
            }  
            });

}