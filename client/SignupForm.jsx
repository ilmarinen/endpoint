import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall} from "./ajax";


class SignupForm extends Component {
  constructor() {
    super();
    this.state = {
      username: "",
      firstName: "",
      lastName: "",
      email: "",
      passwordFirst: "",
      passwordSecond: "",
      passwordsMismatch: false,
      usernameRequired: false
    };

    this.handleUsernameChange = this.handleUsernameChange.bind(this);
    this.handleFirstnameChange = this.handleFirstnameChange.bind(this);
    this.handleLastnameChange = this.handleLastnameChange.bind(this);
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handleRestaurantOwnerChange = this.handleRestaurantOwnerChange.bind(this);
    this.handlePasswordFirstChange = this.handlePasswordFirstChange.bind(this);
    this.handlePasswordSecondChange = this.handlePasswordSecondChange.bind(this);
    this.createUser = this.createUser.bind(this);
  }

  handleUsernameChange(event) {
    this.setState({
      username: event.target.value
    });
  }

  handleFirstnameChange(event) {
    this.setState({
      firstName: event.target.value
    });
  }

  handleLastnameChange(event) {
    this.setState({
      lastName: event.target.value
    });
  }

  handleEmailChange(event) {
    this.setState({
      email: event.target.value
    });
  }

  handleRestaurantOwnerChange(evt) {
    this.setState({
      restaurantowner: !this.state.restaurantowner
    });
  }

  handlePasswordFirstChange(event) {
    this.setState({
      passwordFirst: event.target.value
    });
  }

  handlePasswordSecondChange(event) {
    this.setState({
      passwordSecond: event.target.value
    });
  }

  createUser() {
    this.props.doSignup(
      this.state.username,
      this.state.passwordFirst,
      this.state.firstName,
      this.state.lastName,
      this.state.email,
      this.state.restaurantowner);
  }

  render() {

    let warningComponent;

    if (this.state.passwordMismatch) {
      warningComponent = (
          <div className="form-group">
            <div>Passwords don't match.</div>
          </div>
      );
    } else if (this.state.usernameRequired) {
      warningComponent = (
          <div className="form-group">
            <div>Username is required.</div>
          </div>
      );
    }

    return (
      <form action="#">

          {warningComponent}

          <div className="form-group">
          <label htmlFor="Username">Username</label>
          <input type="text" className="form-control" id="username" onChange={this.handleUsernameChange} />
          </div>

          <div className="form-group">
          <label htmlFor="FirstName">First Name</label>
          <input type="text" className="form-control" id="firstname" onChange={this.handleFirstnameChange} />
          </div>

          <div className="form-group">
          <label htmlFor="LastName">Last Name</label>
          <input type="text" className="form-control" id="lastname" onChange={this.handleLastnameChange} />
          </div>

          <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input type="email" className="form-control" id="email" onChange={this.handleEmailChange} />
          </div>

          <div className="form-group">
          <label htmlFor="email">Restaurant Owner</label>
          &nbsp;
          <input type="checkbox" name="restaurantowner" onChange={this.handleRestaurantOwnerChange} />
          </div>

          <div className="form-group">
          <label htmlFor="pwd">Password:</label>
          <input type="password" className="form-control" id="pwd-first" onChange={this.handlePasswordFirstChange} />
          </div>

          <div className="form-group">
          <label htmlFor="pwd">Confirm Password:</label>
          <input type="password" className="form-control" id="pwd-second" onChange={this.handlePasswordSecondChange} />
          </div>



          <button type="submit" className="btnSubmit" onClick={this.createUser}>Submit</button>

      </form>
    );
  }
}

export default SignupForm;
