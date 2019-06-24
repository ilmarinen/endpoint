import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";
import NewMeal from "./NewMeal.jsx";


class Restaurant extends Component {

  constructor(props) {
    super(props);
    this.state = {
      mealEditor: false
    };
    this.addMealToOrder = this.addMealToOrder.bind(this);
  }

  addMealToOrder(meal) {
    var _this = this;
    return function() {
      _this.props.addMealToOrder(meal);
    }
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

    let mealComponents = this.props.restaurant.meals.map(function(mealData) {
      return (
        <div key={mealData.id} className="card mb-3" onClick={_this.addMealToOrder(mealData)}>
          <h6>{mealData.name}</h6>
          <h6>{mealData.description}</h6>
          <h6>{mealData.price}</h6>
        </div>
      );
    });



    return (
     <div className="card text-success mb-3">
       <div className="card-header">{this.props.restaurant.name}</div>
        <div className="card-body">
           <h5 className="card-title">{this.props.restaurant.description}</h5>
           {mealComponents}
        </div>
      </div>
    );
  }
}
export default Restaurant;
