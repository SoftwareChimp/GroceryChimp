/*
    THIS CODE IS TO MANAGE COOKIES WHICH DETERMINES IF A USER IS SIGNED IN OR NOT.
*/
function get_user() {
    const name = "user";
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                cookieValue = JSON.parse(cookieValue);
                break;
            }
        }
    }
    return cookieValue;
}

function sign_in(user) {
    // SET COOKIE WITH 1 HOUR LIFESPAN
    let d = new Date();
    d.setTime(d.getTime() + (60 * 60 * 1000))
    document.cookie = "user=" + user + "; expires=" + d.toUTCString() + "; path=/";
}

function sign_out() {
    // DELETE COOKIE
    document.cookie = "user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
}

function modify_sign_in() {
    const user = get_user();
    if (user) {
        // THERE IS A USER LOGGED IN
        const elem = document.getElementById("signin-signout");
        elem.innerText = "Hello, " + user["user_first"] + " " + user["user_last"] + " (Sign Out)";
        elem.onclick = () => {
            sign_out();
            console.log("sign out");
            location.reload();
        };
        elem.href = "";
    }
}

function is_signed_in() {
    const user = get_user();
    return user;
}