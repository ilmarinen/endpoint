import React, { Component } from "react";
import ReactDOM from "react-dom";
class NavLoginSignup extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  componentDidMount() {
    this.props.checkAuthenticated();
  }

  render() {
    return (
      <ul className="nav nav-pills" >
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.props.selectSignup}>Signup</a></li>
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.props.selectLogin}>Login</a></li>
      </ul>
    );
  }
}
export default NavLoginSignup;
