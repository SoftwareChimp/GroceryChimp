import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class SignInForm extends Component {
    constructor(){
        super();

        this.state = {
            username: '',
            password: ''
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
              <form onSubmit={this.handleSubmit} className="FormFields" onSubmit={this.handleSubmit}> 
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
                  <button className="FormField_Button" mr-20>Sign In</button>
                  <Link to="/" className="FormField_Link">Create an account</Link>
                </div>
              </form>
            </div>
        );
    }
     
}

export default SignInForm;