import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link, NavLink} from 'react-router-dom';
import SignUpForm from './signin-signup_pages/SignUpForm';
import SignInForm from './signin-signup_pages/SignInForm';
import logo from './images/logo_grocery.png';

import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
      <div className="App_Aside">
        <img className="Logo" src={logo} alt="Logo" />;
      </div>
      <div className="App_Form">
        <div className="PageSwitcher">
          <NavLink exact to="/" activeClassName="PageSwitcher_Item_Active" className="PageSwitcher_Item">Sign Up</NavLink> 
          <NavLink to ="/sign-in" activeClassName="PageSwitcher_Item_Active" className="PageSwitcher_Item">Sign In</NavLink> 
        </div>
        <div className="FormTitle">
          <NavLink to="/sign-in" activeClassName="FormTitle_Link_Active" className="FormTitle_Link">Sign In</NavLink> or
          <NavLink exact to ="/" activeClassName="FormTitle_Link_Active"  className="FormTitle_Link">Sign Up</NavLink>
        </div>
        <Route exact path="/" component={SignUpForm}>
        </Route>
        <Route path="/sign-in" component={SignInForm}>
        </Route>      
      </div>
      </div>
    </Router>
  );
}

export default App;
