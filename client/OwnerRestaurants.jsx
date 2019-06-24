import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";
import OwnerRestaurant from "./OwnerRestaurant.jsx";


class OwnerRestaurants extends Component {

  constructor(props) {
    super(props);
    this.state = {
      newRestaurantName: "",
      newRestaurantDescription: ""
    };
    this.handleNameChange = this.handleNameChange.bind(this);
    this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
    this.handleRestaurantCreate = this.handleRestaurantCreate.bind(this);
  }

  handleDescriptionChange(event) {
    this.setState({
      newRestaurantDescription: event.target.value 
    });
  }

  handleNameChange(event) {
    this.setState({
      newRestaurantName: event.target.value 
    });
  }

  handleRestaurantCreate() {
    this.props.createRestaurant(this.state.newRestaurantName, this.state.newRestaurantDescription);
    this.setState({
      newRestaurantName: "",
      newRestaurantDescription: ""
    })
  }

  render() {
    var _this = this;

    let restaurantComponents

    var cardStyle = {
      "maxWidth": "18rem"
    };
    let styleHR = {
      width: "100%"
    }

    restaurantComponents = this.props.restaurants.map(function(restaurantData) {
       return (
          <OwnerRestaurant restaurant={restaurantData} key={restaurantData.id} createRestaurantMeal={_this.props.createRestaurantMeal} addMealToOrder={_this.props.addMealToOrder} />
       );
    });

    return (
      <div className="container">
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3" style={cardStyle}>
            <div className="card-header">
              <div className="card-header">{this.props.title}</div>
            </div>
            <div className="row">
            <h1 style={styleHR}>My Restaurants</h1>
                <input type="text" className="form-control form-field" placeholder="Name" onChange={this.handleNameChange} value={this.state.newRestaurantName} />
                <input type="text" className="form-control form-field" placeholder="Description" onChange={this.handleDescriptionChange} value={this.state.newRestaurantDescription} />
                <button className="btn btn-success" onClick={this.handleRestaurantCreate}>New Restaurant</button>
            </div>
            <div className="card-body tedxt-primary">
              {restaurantComponents}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default OwnerRestaurants;
