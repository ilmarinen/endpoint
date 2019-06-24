import React, { Component } from "react";
import ReactDOM from "react-dom";
import { bindActionCreators } from "redux";
import { connect } from 'react-redux';
import { AnonymousSignup, AnonymousLogin } from "./AnonymousViews.jsx";
import {
  selectLogin,
  selectSignup,
  selectMyOrders,
  selectRestaurantOrders,
  selectRestaurants,
  selectOwnerRestaurants,
  selectProfile,
  loginRequested,
  loginSuccessful,
  loginFailed,
  doLogin,
  checkAuthenticated,
  updateUser,
  doLogout,
  doSignup,
  createRestaurant,
  createRestaurantMeal,
  addMealToOrder,
  placeOrder,
  cancelUnplacedOrder,
  getMyOrders,
  getIncomingOrders,
  incrementMyOrderStatus,
  incrementIncomingOrderStatus
} from '../actions.js';


function Container({
  session,
  checkAuthenticated,
  selectLogin,
  selectSignup,
  doLogin,
  doLogout,
  doSignup}) {

    return (
        <AnonymousLogin
          selectLogin={selectLogin} selectSignup={selectSignup} checkAuthenticated={checkAuthenticated}
          doLogin={doLogin}
        />
      );

}

function mapStateToProps (state) {
  return {
    session: state.session,
  };
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators({
    selectLogin: selectLogin,
    selectSignup: selectSignup,
    doLogin: doLogin,
    checkAuthenticated: checkAuthenticated,
    doLogout: doLogout,
    doSignup: doSignup,
  }, dispatch);
 }

const LoginContainer = connect(mapStateToProps, mapDispatchToProps)(Container)

export default LoginContainer;
