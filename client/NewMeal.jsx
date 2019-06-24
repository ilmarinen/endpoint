import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";


class NewMeal extends Component {

  constructor(props) {
    super(props);
    this.state = {
      newMealName: "",
      newMealDescription: "",
      newMealPrice: ""
    };

    this.handleNameChange = this.handleNameChange.bind(this);
    this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
    this.handleRestaurantMealCreate = this.handleRestaurantMealCreate.bind(this);
    this.handlePriceChange = this.handlePriceChange.bind(this);
  }

  handleNameChange(event) {
    this.setState({
      newMealName: event.target.value
    });
  }

  handleDescriptionChange(event) {
    this.setState({
      newMealDescription: event.target.value
    });
  }

  handlePriceChange(event) {
    this.setState({
      newMealPrice: event.target.value
    });
  }

  handleRestaurantMealCreate() {
    this.props.createRestaurantMeal(this.props.restaurant.id, this.state.newMealName, this.state.newMealDescription, this.state.newMealPrice);
    this.props.toggleMealEditor();
  }

  render() {

    let restaurantComponents

    var cardStyle = {
      "maxWidth": "18rem"
    };
    let styleHR = {
      width: "100%"
    }


    return (
      <div className="card mb-3">
        <input type="text" className="form-control form-field" placeholder="Name" onChange={this.handleNameChange} value={this.state.newMealName} />
        <input type="text" className="form-control form-field" placeholder="Description" onChange={this.handleDescriptionChange} value={this.state.newMealDescription} />
        <input type="text" className="form-control form-field" placeholder="Price" onChange={this.handlePriceChange} value={this.state.newMealPrice} />
        <button className="btn btn-success" onClick={this.handleRestaurantMealCreate}>New Meal</button> 
      </div>
    );
  }
}
export default NewMeal;
