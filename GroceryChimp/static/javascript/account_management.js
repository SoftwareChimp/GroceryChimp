/*
    THIS CODE IS TO MANAGE COOKIES WHICH DETERMINES IF A USER IS SIGNED IN OR NOT.
*/
function getUser() {
    const name = "user";
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function signIn(user) {
    // SET COOKIE WITH 1 HOUR LIFESPAN
    let d = new Date();
    d.setTime(d.getTime() + (60 * 60 * 1000))
    document.cookie = "user=" + user + "; expires=" + d.toUTCString() + "; path=/";
}

function signOut() {
    // DELETE COOKIE
    document.cookie = "user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
}

function modifySignIn() {
    const user = getUser();
    if (user) {
        // THERE IS A USER LOGGED IN
        const elem = document.getElementById("signin-signout");
        elem.innerText = "Hello, " + user + " (Sign Out)";
        elem.onclick = () => {
            signOut();
            console.log("sign out");
            location.reload();
        };
        elem.href = "";
    }
}

function isSignedIn() {
    const user = getUser();
    return user;
}