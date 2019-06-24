import React, { Component } from "react";
import ReactDOM from "react-dom";
import UserProfile from "../UserProfile.jsx";
import {makePostCall, makeGetCall} from "../ajax";
import { bindActionCreators } from "redux";
import { connect } from 'react-redux';
import { OwnerProfileView, OwnerOrdersView, OwnerRestaurantsView } from "./OwnerViews.jsx";
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
  selectedTab,
  session,
  restaurants,
  ownerRestaurants,
  orders,
  unplacedOrders,
  restaurantOrders,
  checkAuthenticated,
  selectLogin,
  selectSignup,
  selectRestaurants,
  selectOwnerRestaurants,
  selectProfile,
  selectMyOrders,
  selectRestaurantOrders,
  doLogin,
  updateUser,
  doLogout,
  doSignup,
  createRestaurant,
  createRestaurantMeal,
  addMealToOrder,
  cancelUnplacedOrder,
  placeOrder,
  getMyOrders,
  getIncomingOrders,
  incrementMyOrderStatus,
  incrementIncomingOrderStatus}) {
    if (session.authenticated && session.user.restaurant_owner && selectedTab == "PROFILE") {
      return (
        <OwnerProfileView
          user={session.user}
          selectRestaurants={selectRestaurants}
          selectOwnerRestaurants={selectOwnerRestaurants}
          selectProfile={selectProfile}
          selectMyOrders={getMyOrders}
          selectRestaurantOrders={getIncomingOrders}
          updateUser={updateUser} logoutHandler={doLogout}
        />
      );
    } else if (session.authenticated && session.user.restaurant_owner && selectedTab == "OWNER_RESTAURANTS") {
        return (
          <OwnerRestaurantsView
            user={session.user}
            selectRestaurants={selectRestaurants}
            selectOwnerRestaurants={selectOwnerRestaurants}
            selectProfile={selectProfile}
            selectRestaurantOrders={getIncomingOrders}
            title="My restaurants" restaurants={ownerRestaurants} createRestaurant={createRestaurant} createRestaurantMeal={createRestaurantMeal}
          />
        );
    } else if (session.authenticated && session.user.restaurant_owner && selectedTab == "RESTAURANT_ORDERS") {
        return (
          <OwnerOrdersView
            user={session.user}
            selectRestaurants={selectRestaurants}
            selectOwnerRestaurants={selectOwnerRestaurants}
            selectProfile={selectProfile}
            selectRestaurantOrders={getIncomingOrders}
            getIncomingOrders={getIncomingOrders}
            restaurantOrders={restaurantOrders}
            incrementIncomingOrderStatus={incrementIncomingOrderStatus}
          />
        );
    }
}

function mapStateToProps (state) {
  return {
    selectedTab: state.rootReducer.selectedTab,
    session: state.rootReducer.session,
    restaurants: state.rootReducer.restaurants,
    ownerRestaurants: state.rootReducer.ownerRestaurants,
    orders: state.rootReducer.orders,
    restaurantOrders: state.rootReducer.restaurantOrders,
    unplacedOrders: state.rootReducer.unplacedOrders
  };
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators({
    selectLogin: selectLogin,
    selectSignup: selectSignup,
    doLogin: doLogin,
    checkAuthenticated: checkAuthenticated,
    updateUser: updateUser,
    doLogout: doLogout,
    doSignup: doSignup,
    selectProfile: selectProfile,
    selectRestaurants: selectRestaurants,
    selectOwnerRestaurants: selectOwnerRestaurants,
    selectMyOrders: selectMyOrders,
    selectRestaurantOrders: selectRestaurantOrders,
    createRestaurant: createRestaurant,
    createRestaurantMeal: createRestaurantMeal,
    addMealToOrder: addMealToOrder,
    cancelUnplacedOrder: cancelUnplacedOrder,
    placeOrder: placeOrder,
    getMyOrders: getMyOrders,
    getIncomingOrders: getIncomingOrders,
    incrementMyOrderStatus: incrementMyOrderStatus,
    incrementIncomingOrderStatus: incrementIncomingOrderStatus
  }, dispatch);
 }

const OwnerContainer = connect(mapStateToProps, mapDispatchToProps)(Container)

export default OwnerContainer;
