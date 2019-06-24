import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";
import Upload from "./Upload.jsx";


class UserProfile extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: this.props.user,
      editUser: false,
      editUserId: this.props.user.id,
      editUserUsername: this.props.user.username,
      editUserFirstName: this.props.user.firstname,
      editUserLastName: this.props.user.lastname,
    };

  this.updateUser = this.updateUser.bind(this);
  this.editUser = this.editUser.bind(this);
  this.handleFirstNameChange = this.handleFirstNameChange.bind(this);
  this.handleLastNameChange = this.handleLastNameChange.bind(this);
  this.logout = this.logout.bind(this);
  this.reload = this.reload.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      user: nextProps.user,
      editUser: false,
      editUserId: nextProps.user.id,
      editUserUsername: nextProps.user.username,
      editUserFirstName: nextProps.user.firstName,
      editUserLastName: nextProps.user.lastName,
    });
  }

  handleFirstNameChange(evt) {
    this.setState({
      editUserFirstName: evt.target.value,
    });
  }

  handleLastNameChange(evt) {
    this.setState({
      editUserLastName: evt.target.value
    });
  }

  editUser(evt) {
    var user = this.state.user;
    this.setState({
      editUser: true
    });
  }

  updateUser() {
    this.props.updateUser(this.state.editUserId, this.state.editUserFirstName, this.state.editUserLastName)
  }

  logout(e) {
    e.stopPropagation();
    this.props.logoutHandler();
  }

  reload() {
    this.props.reloadProfile();
  }

  render() {
    var _this = this;

    var cardStyle = {
      "maxWidth": "18rem"
    };

    const profileImage = (this.props.user.profile_filename != "" && this.props.user.profile_filename != null)?("uploads/" + this.props.user.profile_filename):"static/profile.png";

    if (!this.state.editUser) {
      return (
        <div className="container">
          <div className="row">
            <div className="card info-card bg-border-secondary mb-3" style={cardStyle} onClick={this.editUser}>
              <div className="card-header">{this.state.user.username}</div>
              <div className="card-body tedxt-primary">
                <img width="200px" height="200px" src={profileImage} />
                <h6 className="card-text">{this.state.user.firstname}</h6>
                <h6 className="card-text">{this.state.user.lastname}</h6>
                <a href="#" className="btn btn-primary" onClick={this.logout}>Logout</a>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="container">
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3" style={cardStyle}>
            <div className="card-header">
              <div className="card-header">{this.state.user.username}</div>
            </div>
            <div className="card-body tedxt-primary">
              <Upload reload={this.reload} />
              <input type="text" className="form-control form-field" onChange={this.handleFirstNameChange} value={this.state.editUserFirstName} />
              <input type="text" className="form-control form-field" onChange={this.handleLastNameChange} value={this.state.editUserLastName} />
              <a href="#" className="btn btn-primary" onClick={this.updateUser}>Update</a>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default UserProfile;
