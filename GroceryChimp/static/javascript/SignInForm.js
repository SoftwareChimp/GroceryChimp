'use strict';

const e = React.createElement;

class SignIn extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: ''
        };
        this.errorString = "";
    }

    handleChange = (e) => {
        let target = e.target;
        this.setState({
            [target.name]: target.value
        });
    }

    handleSubmit = (e) => {
        e.preventDefault();
        // STOP CODE IF EMPTY FIELDS
        if (!this.state.username.length || !this.state.password.length) {
            return;
        }

        fetch('/signin/', {
            credentials: 'include',
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify(this.state),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
            .then(res => res.json())
            .then((response) => {
                console.log('post success', JSON.stringify(response));

                // REFRESH RENDER IF ERROR
                if (response["error"]) {
                    console.log("error found");
                    this.errorString = response["error"];
                    this.setState(prevState => ({
                        username: prevState.username,
                        password: prevState.password
                    }));
                }
                else if (response["success"]) {
                    console.log("login successful");
                    // SET COOKIE
                    let d = new Date();
                    d.setTime(d.getTime() + (60 * 60 * 1000)) // EXPIRE IN 1 HOUR
                    document.cookie = "user=" + JSON.stringify(response["success"]) + "; expires=" + d.toUTCString() + "; path=/";

                    // REDIRECT USER BACK TO HOME PAGE
                    window.location.replace("/");
                }
            });
    }

    render() {
        return e('div', {class:"FormCenter"},
            e('form', {onSubmit:this.handleSubmit, class:"FormFields"}, [
                e('div', {class:"FormField"}, [
                    e('label', {class:"FormField_Label", htmlFor:"username"}, "USERNAME"),
                    e('input', {type:"text", id:"username", class:"FormField_Input",
                                placeholder:"Enter your username", name:"username", value:this.state.username,
                                onChange:this.handleChange})
                ]),
                e('div', {class:"FormField"}, [
                    e('label', {class:"FormField_Label", htmlFor:"password"}, "PASSWORD"),
                    e('input', {type:"password", id:"password", class:"FormField_Input",
                                placeholder:"Enter your password", name:"password", value:this.state.password,
                                onChange:this.handleChange})
                ]),
                e('div', {class:"FormField"}, [
                    e('button', {class:"FormField_Button mr-20"}, "Sign In"),
                    e('a', {href:"/signup", class:"FormField_Link"}, "Create an account")
                ]),
                // LOG IN ERROR DISPLAYED HERE
                e('div', {class:"FormField"}, [
                    e('span', {class:"FormField_Label"}, this.errorString),
                ]),
            ])
        );
    }
}
ReactDOM.render(e(SignIn), document.querySelector('#root'));