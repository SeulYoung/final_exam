function login_check() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let email_valid = /^[0-9a-zA-Z\_\-]+(\.[0-9a-zA-Z\_\-]+)*@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,}$/;
    let username_valid = /^[a-z]+$/;

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