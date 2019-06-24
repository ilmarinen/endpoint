import React, { Component } from "react";
import ReactDOM from "react-dom";
class NavOrders extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
    this.ownerRestaurants = this.ownerRestaurants.bind(this);
    this.selectMyOrders = this.selectMyOrders.bind(this);
  }

  ownerRestaurants() {
    this.props.selectOwnerRestaurants(this.props.user.id);
  }

  selectMyOrders() {
    this.props.selectMyOrders(this.props.user.id);
  }

  render() {

    if (this.props.user.restaurant_owner) {
      return (
      <ul className="nav nav-pills" >
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.ownerRestaurants}>Restaurants</a></li>
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.props.selectRestaurantOrders}>Orders</a></li>
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.props.selectProfile}>Profile</a></li>
      </ul>
      );
    }
    return (
      <ul className="nav nav-pills" >
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.selectMyOrders}>Orders</a></li>
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.props.selectRestaurants}>Restaurants</a></li>
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.props.selectProfile}>Profile</a></li>
      </ul>
    );
  }
}
export default NavOrders;
