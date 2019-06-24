import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";


class MyOrders extends Component {

  constructor(props) {
    super(props);
    this.timeoutVar = null;
    this.pollMyOrders = this.pollMyOrders.bind(this);
  }

  componentDidMount() {
    this.pollMyOrders();
  }

  componentWillUnmount() {
    clearTimeout(this.timeoutVar);
  }

  pollMyOrders() {
    this.props.getMyOrders(this.props.user.id);
    this.timeoutVar = setTimeout(this.pollMyOrders, 5000);
  }

  cancelUnplacedOrder(restaurantId) {
    var _this = this;
    return function() {
      _this.props.cancelUnplacedOrder(restaurantId);
    }
  }

  placeOrder(restaurantId, unplacedOrderData) {
    var _this = this;
    return function() {
      _this.props.placeOrder(_this.props.user.id, restaurantId, unplacedOrderData);
    }
  }

  incrementMyOrderStatus(orderId) {
    var _this = this;

    return function() {
      _this.props.incrementMyOrderStatus(_this.props.user.id, orderId);
    }
  }

  render() {
    var _this = this;

    var cardStyle = {
      "maxWidth": "18rem"
    };

    let unplacedOrderComponents = Object.keys(this.props.unplacedOrders).map(function(restaurantId) {
      let unplacedOrderData = _this.props.unplacedOrders[restaurantId];
      let total = 0;
      let mealComponents = Object.keys(unplacedOrderData).map(function(mealId) {
        total += unplacedOrderData[mealId].price;
        return (
          <h5>{unplacedOrderData[mealId].name} {unplacedOrderData[mealId].price}</h5>
        );
      });

      return (
       <div className="card text-success mb-3">
         <div className="card-header">Order</div>
          <div className="card-body">
             {mealComponents}
             <h6>Amount: {total}</h6>
          </div>
          <button className="btn btn-success" onClick={_this.placeOrder(restaurantId, unplacedOrderData)}>Place</button>
          <button className="btn btn-danger" onClick={_this.cancelUnplacedOrder(restaurantId)}>Cancel</button>
        </div>
      );
    });

    let placedOrderComponents = this.props.orders.map(function(orderData) {
      let orderStatus = [<h7>Placed</h7>, <h7>Canceled</h7>, <h7>Processing</h7>, <h7>Enroute</h7>, <h7>Delivered</h7>, <h7>Received</h7>];

      let mealComponents = orderData.meals.map(function(mealData) {
        return (
          <h5>{mealData.name}</h5>
        );
      });

      return (
       <div className="card text-success mb-3">
         <div className="card-header">Order</div>
          <div className="card-body">
             {mealComponents}
             <h6>Amount: {orderData.amount}</h6>
          </div>
          <div onClick={_this.incrementMyOrderStatus(orderData.id)}>
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
              <div className="card-header">Your orders</div>
            </div>
            <div className="card-body text-primary">
              {unplacedOrderComponents}
            </div>
            <div className="card-body text-primary">
              {placedOrderComponents}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default MyOrders;
