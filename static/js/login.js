function login_check() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let email_valid = /^[0-9a-z\_\-]+(\.[0-9a-z\_\-]+)*@[0-9a-z]+(\.[0-9a-z]+){1,}$/;
    let username_valid = /^[a-z0-9\-\_]+$/;

    if (!email_valid.test(email) && !username_valid.test(email)) {
        document.getElementById('error').innerHTML = 'enter a valid email address/username.';
        return false;
    }
    if (password.length < 6) {
        document.getElementById("error").innerHTML = "password too short.";
        return false;
    }
    return true;
}