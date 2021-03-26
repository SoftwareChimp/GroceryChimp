'use strict';

const e = React.createElement;

class SignUp extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            firstname: '',
            lastname: '',
            username: '',
            password: '',
            email: '',
            phoneNumber: '',
            address: ''
        };
        this.errorString = "";

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
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
        if (!this.state.firstname.length || !this.state.lastname.length ||
            !this.state.username.length || !this.state.password.length ||
            !this.state.email.length || !this.state.phoneNumber.length ||
            !this.state.address.length) {
            return;
        }

        fetch('/signup/', {
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
                        firstname: prevState.firstname,
                        lastname: prevState.lastname,
                        username: prevState.username,
                        password: prevState.password,
                        email: prevState.email,
                        phoneNumber: prevState.phoneNumber,
                        address: prevState.address
                    }));
                }
                else if (response["success"]) {
                    console.log("account creation successful");
                    // SET COOKIE
                    let d = new Date();
                    d.setTime(d.getTime() + (60 * 60 * 1000)) // EXPIRE IN 1 HOUR
                    document.cookie = "user=" + response["success"] + "; expires=" + d.toUTCString() + "; path=/";

                    // REDIRECT USER BACK TO HOME PAGE
                    window.location.replace("/");
                }
            });
    }

    render() {
        return e('div', {class:"FormCenter"},
            e('form', {onSubmit:this.handleSubmit, class:"FormFields"}, [
                e('div', {class:"FormField"}, [
                    e('label', {class:"FormField_Label", htmlFor:"firstname"}, "FIRST NAME"),
                    e('input', {type:"text", id:"firstname", class:"FormField_Input",
                                placeholder:"Enter your first name", name:"firstname", value:this.state.firstname,
                                onChange:this.handleChange})
                ]),
                e('div', {class:"FormField"}, [
                    e('label', {class:"FormField_Label", htmlFor:"lastname"}, "LAST NAME"),
                    e('input', {type:"text", id:"lastname", class:"FormField_Input",
                                placeholder:"Enter your last name", name:"lastname", value:this.state.lastname,
                                onChange:this.handleChange})
                ]),
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
                    e('label', {class:"FormField_Label", htmlFor:"email"}, "EMAIL ADDRESS"),
                    e('input', {type:"email", id:"email", class:"FormField_Input",
                                placeholder:"Enter your email", name:"email", value:this.state.email,
                                onChange:this.handleChange})
                ]),
                e('div', {class:"FormField"}, [
                    e('label', {class:"FormField_Label", htmlFor:"phoneNumber"}, "PHONE NUMBER"),
                    e('input', {type:"text", id:"phoneNumber", class:"FormField_Input",
                                placeholder:"Enter your phone number", name:"phoneNumber", value:this.state.phoneNumber,
                                onChange:this.handleChange})
                ]),
                e('div', {class:"FormField"}, [
                    e('label', {class:"FormField_Label", htmlFor:"address"}, "ADDRESS"),
                    e('input', {type:"text", id:"address", class:"FormField_Input",
                                placeholder:"Enter your address", name:"address", value:this.state.address,
                                onChange:this.handleChange})
                ]),
                e('div', {class:"FormField"}, [
                    e('button', {class:"FormField_Button mr-20"}, "Sign Up"),
                    e('a', {href:"/signin", class:"FormField_Link"}, "I'm already a member")
                ]),
                // LOG IN ERROR DISPLAYED HERE
                e('div', {class:"FormField"}, [
                    e('span', {class:"FormField_Label"}, this.errorString),
                ]),
            ])
        );
    }
}
ReactDOM.render(e(SignUp), document.querySelector('#root'));