import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";


class RestaurantOrders extends Component {

  constructor(props) {
    super(props);
    this.timeoutVar = null;
    this.pollIncomingOrders = this.pollIncomingOrders.bind(this);
  }

  componentDidMount() {
    this.pollIncomingOrders();
  }

  componentWillUnmount() {
    clearTimeout(this.timeoutVar);
  }

  pollIncomingOrders() {
    this.props.getIncomingOrders(this.props.user.id);
    this.timeoutVar = setTimeout(this.pollIncomingOrders, 5000);
  }

  cancelUnplacedOrder(restaurantId) {
    var _this = this;
    return function() {
      _this.props.cancelUnplacedOrder(restaurantId);
    }
  }

  incrementIncomingOrderStatus(orderId) {
    var _this = this;

    return function() {
      _this.props.incrementIncomingOrderStatus(_this.props.user.id, orderId);
    }
  }

  render() {
    var _this = this;

    var cardStyle = {
      "maxWidth": "18rem"
    };

    let restaurantOrderComponents = this.props.restaurantOrders.map(function(orderData) {
      let orderStatus = [<h7>Placed</h7>, <h7>Canceled</h7>, <h7>Processing</h7>, <h7>Enroute</h7>, <h7>Delivered</h7>, <h7>Received</h7>];

      let mealComponents = orderData.meals.map(function(mealData) {
        return (
          <h5 key={mealData.id}>{mealData.name}</h5>
        );
      });

      return (
       <div className="card text-success mb-3" key={orderData.id}>
         <div className="card-header">Order</div>
          <div className="card-body">
             {mealComponents}
             <h6>Amount: {orderData.amount}</h6>
          </div>
          <div onClick={_this.incrementIncomingOrderStatus(orderData.id)}>
            {orderStatus[orderData.status]}
          </div>
          {orderData.history.map((orderHistoryRecord) => {
            return (
              <h8>{orderHistoryRecord.status} {orderHistoryRecord.set_at}</h8>
            );
          })}
        </div>
      );
    });

    return (
      <div className="container">
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3" style={cardStyle}>
            <div className="card-header">
              <div className="card-header">Incoming Orders</div>
            </div>
            <div className="card-body tedxt-primary">
              {restaurantOrderComponents}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default RestaurantOrders;
