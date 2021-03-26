/*
    THIS CODE IS TO HANDLE THE CSRFToken NEEDED FOR POST MESSAGES

    GET THE CSRFToken VIA getCookie('csrftoken') THEN FOR HEADERS:
    headers: {
        'X-CSRFToken': "YOUR_CSRF_TOKEN_HERE"
    }

    jQuery IS REQUIRED FOR THIS CODE TO WORK
*/
function getCSRFToken() {
    const name = "csrftoken";
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