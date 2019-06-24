import React, { Component } from "react";
import ReactDOM from "react-dom";
class NavOwners extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
    this.ownerRestaurants = this.ownerRestaurants.bind(this);
    this.selectRestaurantOrders = this.selectRestaurantOrders.bind(this);
  }

  ownerRestaurants() {
    this.props.selectOwnerRestaurants(this.props.user.id);
  }

  selectRestaurantOrders() {
    console.log("Restaurant orders");
    this.props.selectRestaurantOrders(this.props.user.id);
  }

  render() {

    return (
      <ul className="nav nav-pills" >
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.ownerRestaurants}>Restaurants</a></li>
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.selectRestaurantOrders}>Orders</a></li>
          <li className=""><a className="btn btn-lg btn-default" href="#" onClick={this.props.selectProfile}>Profile</a></li>
      </ul>
      );
  }
}
export default NavOwners;
