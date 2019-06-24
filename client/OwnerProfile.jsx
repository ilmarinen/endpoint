import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";
import Upload from "./Upload.jsx";


class OwnerProfile extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: this.props.user,
      editUser: false,
      editUserId: this.props.user.id,
      editUserUsername: this.props.user.username,
      editUserFirstName: this.props.user.firstname,
      editUserLastName: this.props.user.lastname,
      blockUsername: '',
      inviteeEmail: '',
      errorMessage: '',
      blockedUsers: []
    };

  this.updateUser = this.updateUser.bind(this);
  this.editUser = this.editUser.bind(this);
  this.handleFirstNameChange = this.handleFirstNameChange.bind(this);
  this.handleLastNameChange = this.handleLastNameChange.bind(this);
  this.handleBlockUsernameChange = this.handleBlockUsernameChange.bind(this);
  this.handleInviteeEmailChange = this.handleInviteeEmailChange.bind(this);
  this.blockUser = this.blockUser.bind(this);
  this.logout = this.logout.bind(this);
  this.reload = this.reload.bind(this);
  this.blockUser = this.blockUser.bind(this);
  this.inviteUser = this.inviteUser.bind(this);
  this.getBlockedUsers = this.getBlockedUsers.bind(this);
  this.unblockHandlerForUser = this.unblockHandlerForUser.bind(this);
  }

  componentDidMount() {
    this.getBlockedUsers();
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

  handleBlockUsernameChange(evt) {
    this.setState({
      blockUsername: evt.target.value
    });
  }

  handleInviteeEmailChange(evt) {
    this.setState({
      inviteeEmail: evt.target.value
    });
  }

  getBlockedUsers() {
    var _this = this;
    makeGetCall("api/v1/blocked_users",
    ).then(users => {
      _this.setState({
        blockedUsers: users
      });
    })
     .fail(err => {
      _this.setSate({
        errorMessage: "Error getting blocked user"
      })
     });
  }

  blockUser() {
    var _this = this;

    makePostCall("api/v1/blocked_users",
      {
        username: this.state.blockUsername
      }
    ).then(res => {
      _this.getBlockedUsers();
      _this.setState({
        blockUsername: ''
      });
    })
     .fail(err => {
      _this.setSate({
        errorMessage: "Error blocking user"
      })
     });
  }

  inviteUser() {
    var _this = this;

    makePostCall("api/v1/users/" + this.props.user.id + "/invites",
      {
        email: this.state.inviteeEmail
      }
    ).then(res => {
      _this.setState({
        inviteeEmail: ''
      });
    })
     .fail(err => {
      _this.setSate({
        errorMessage: "Error inviting user"
      })
     });
  }

  unblockHandlerForUser(userId) {
    var _this = this;
    return function() {
      makePostCall("api/v1/blocked_users/" + userId,
        {}
      ).then(res => {
        _this.getBlockedUsers()
      })
       .fail(err => {
        _this.setSate({
          errorMessage: "Error unblocking user"
        })
       });
    }
  }

  logout(e) {
    e.stopPropagation();
    this.props.logoutHandler();
  }

  reload() {
    this.setState({
      editUser: !this.state.editUser
    });
    this.props.reloadProfile();
  }

  render() {
    var _this = this;

    var cardStyle = {
      "maxWidth": "18rem"
    };

    let userComponent;
    const profileImage = (this.props.user.profile_filename != "" && this.props.user.profile_filename != null)?("uploads/" + this.props.user.profile_filename):"static/profile.png";

    if (!this.state.editUser) {
      userComponent = (
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3" style={cardStyle} onClick={this.editUser}>
            <div className="card-header">Owner: {this.state.user.username}</div>
            <div className="card-body tedxt-primary">
              <img width="200px" height="200px" src={profileImage} />
              <h6 className="card-text">{this.state.user.firstname}</h6>
              <h6 className="card-text">{this.state.user.lastname}</h6>
              <a href="#" className="btn btn-primary" onClick={this.logout}>Logout</a>
            </div>
          </div>
        </div>
      );
    } else {
      userComponent = (
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
      );
    }

    return (
      <div className="container">
        {userComponent}
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3" style={cardStyle}>
            <div className="card-header">
              <div className="card-header">Block Users</div>
            </div>
            <div className="card-body tedxt-primary">
              <input type="text" className="form-control form-field" onChange={this.handleBlockUsernameChange} value={this.state.blockUsername} />
              <a href="#" className="btn btn-primary" onClick={this.blockUser}>Block</a>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3" style={cardStyle}>
            <div className="card-header">
              <div className="card-header">Invite Users</div>
            </div>
            <div className="card-body tedxt-primary">
              <input type="text" className="form-control form-field" onChange={this.handleInviteeEmailChange} value={this.state.inviteeEmail} />
              <a href="#" className="btn btn-primary" onClick={this.inviteUser}>Invite</a>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3" style={cardStyle}>
            <div className="card-header">
              <div className="card-header">Blocked Users</div>
            </div>
            <div className="card-body tedxt-primary">
              {this.state.blockedUsers.map(user =><h5 key={user.id} onClick={_this.unblockHandlerForUser(user.id)}>{user.username} Unblock</h5>)}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default OwnerProfile;
