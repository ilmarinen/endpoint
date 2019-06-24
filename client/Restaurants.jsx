import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";
import Restaurant from "./Restaurant.jsx";


class Restaurants extends Component {

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
          <Restaurant restaurant={restaurantData} key={restaurantData.id} createRestaurantMeal={_this.props.createRestaurantMeal} addMealToOrder={_this.props.addMealToOrder} />
       );
    });

    return (
      <div className="container">
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3" style={cardStyle}>
            <div className="card-header">
              <div className="card-header">{this.props.title}</div>
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
export default Restaurants;
