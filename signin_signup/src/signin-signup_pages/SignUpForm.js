import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class SignUpForm extends Component {
  constructor(){
    super();

    this.state = {
        firstname: '',
        lastname: '',
        username: '',
        password: '',
        email: '',
        phoneNumber: '',
        address: ''
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

}

handleChange(e){
    // Select target element 
    let target = e.target;
    let value = target.type == 'checkbox' ? target : target.value;
    let name = target.name;

    this.setState({
        [name]: value
    });
}

handleSubmit(e){
  e.preventDefault();

  console.log('The form was submitted with the following data');
  console.log(this.state);
}

    render(){
        return(

            <div className="FormCenter"> 
              <form onSubmit={this.handleSubmit} className="FormFields">
                <div className="FormField">
                  <label className="FormField_Label" htmlFor="firstname">FIRST NAME</label>
                  <input type="text" id="firstname" className="FormField_Input" placeholder="Enter your first name"
                  name="firstname" value={this.state.firstname} onChange={this.handleChange}/>
                </div>
                <div className="FormField">
                  <label className="FormField_Label" htmlFor="lastname">LAST NAME</label>
                  <input type="text" id="lastname" className="FormField_Input" placeholder="Enter your last name" 
                  name="lastname" value={this.state.lastname} onChange={this.handleChange}/>
                </div>
                <div className="FormField">
                  <label className="FormField_Label" htmlFor="username">USERNAME</label>
                  <input type="text" id="username" className="FormField_Input" placeholder="Enter your username" 
                  name="username" value={this.state.username} onChange={this.handleChange}/>
                </div>
                <div className="FormField">
                  <label className="FormField_Label" htmlFor="password">PASSWORD</label>
                  <input type="password" id="password" className="FormField_Input" placeholder="Enter your password" 
                  name="password" value={this.state.password} onChange={this.handleChange}/>
                </div>
                <div className="FormField">
                  <label className="FormField_Label" htmlFor="email">EMAIL ADDRESS</label>
                  <input type="email" id="email" className="FormField_Input" placeholder="Enter your email" 
                  name="email" value={this.state.email} onChange={this.handleChange}/>
                </div>
                <div className="FormField">
                  <label className="FormField_Label" htmlFor="phoneNumber">PHONE NUMBER</label>
                  <input type="text" id="phoneNumber" className="FormField_Input" placeholder="Enter your phone number" 
                  name="phoneNumber" value={this.state.phoneNumber} onChange={this.handleChange}/>
                </div>
                <div className="FormField">
                  <label className="FormField_Label" htmlFor="address">ADDRESS</label>
                  <input type="text" id="address" className="FormField_Input" placeholder="Enter your address" 
                  name="address" value={this.state.address} onChange={this.handleChange}/>
                </div>

                <div className="FormField">
                  <button className="FormField_Button" mr-20>Sign Up</button>
                  <Link to="/sign-in" className="FormField_Link">I'm already a member</Link>
                </div>
              </form>
            </div>


        );
    }
     
}

export default SignUpForm;