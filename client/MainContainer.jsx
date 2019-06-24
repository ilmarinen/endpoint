import React, { Component } from "react";
import ReactDOM from "react-dom";
import LoginForm from "./LoginForm.jsx";
import SignupForm from "./SignupForm.jsx";
import NavLoginSignup from "./NavLoginSignup.jsx";
import NavOrders from "./NavOrders.jsx";
import NavOwners from "./NavOwners.jsx";
import UserProfile from "./UserProfile.jsx";
import OwnerProfile from "./OwnerProfile.jsx";
import MyOrders from "./MyOrders.jsx"
import Restaurants from "./Restaurants.jsx";
import OwnerRestaurants from "./OwnerRestaurants.jsx";
import RestaurantOrders from "./RestaurantOrders.jsx";
import {makePostCall, makeGetCall} from "./ajax";
import { bindActionCreators } from "redux";
import { connect } from 'react-redux';
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
} from './actions.js';


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
    let formComponent;
    let navComponent;

    if (!session.authenticated) {
      navComponent = <NavLoginSignup selectLogin={selectLogin} selectSignup={selectSignup} checkAuthenticated={checkAuthenticated} />;
    } else if (!session.user.restaurant_owner) {
      navComponent = <NavOrders
                       user={session.user}
                       selectRestaurants={selectRestaurants}
                       selectOwnerRestaurants={selectOwnerRestaurants}
                       selectProfile={selectProfile}
                       selectMyOrders={getMyOrders}
                       selectRestaurantOrders={selectRestaurantOrders} />;
    } else if (session.user.restaurant_owner) {
      navComponent = <NavOwners
                       user={session.user}
                       selectOwnerRestaurants={selectOwnerRestaurants}
                       selectProfile={selectProfile}
                       selectRestaurantOrders={getIncomingOrders} />;
    }

    if (selectedTab == "SIGNUP") {
      formComponent = <SignupForm selectLogin={selectLogin} doSignup={doSignup} />;
    } else if (selectedTab == "LOGIN") {
      formComponent = <LoginForm loginHandler={doLogin} />;
    } else if (selectedTab == "PROFILE" && !session.user.restaurant_owner) {
      formComponent = <UserProfile user={session.user} updateUser={updateUser} logoutHandler={doLogout} reloadProfile={checkAuthenticated} />;
    } else if (selectedTab == "PROFILE" && session.user.restaurant_owner) {
      formComponent = <OwnerProfile user={session.user} updateUser={updateUser} logoutHandler={doLogout} reloadProfile={checkAuthenticated} />;
    } else if (selectedTab == "RESTAURANTS") {
      formComponent = <Restaurants title="All restaurants" restaurants={restaurants} addMealToOrder={addMealToOrder} />;
    } else if (selectedTab == "MY_ORDERS") {
      formComponent = <MyOrders 
                        orders={orders}
                        unplacedOrders={unplacedOrders}
                        user={session.user}
                        getMyOrders={getMyOrders}
                        placeOrder={placeOrder}
                        cancelUnplacedOrder={cancelUnplacedOrder}
                        incrementMyOrderStatus={incrementMyOrderStatus} />;
    } else if (selectedTab == "OWNER_RESTAURANTS") {
      formComponent = <OwnerRestaurants title="My restaurants" restaurants={ownerRestaurants} createRestaurant={createRestaurant} createRestaurantMeal={createRestaurantMeal} />;
    } else if (selectedTab == "RESTAURANT_ORDERS") {
      formComponent = <RestaurantOrders
                         user={session.user}
                         getIncomingOrders={getIncomingOrders}
                         restaurantOrders={restaurantOrders}
                         incrementIncomingOrderStatus={incrementIncomingOrderStatus} />;
    }

    return (
      <div className="container">
          <div className="row">
              <div className="col-md-6">
                  {navComponent}
                  {formComponent}
              </div>
          </div>
      </div>
    );
}

function mapStateToProps (state) {
  return {
    selectedTab: state.selectedTab,
    session: state.session,
    restaurants: state.restaurants,
    ownerRestaurants: state.ownerRestaurants,
    orders: state.orders,
    restaurantOrders: state.restaurantOrders,
    unplacedOrders: state.unplacedOrders
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

const MainContainer = connect(mapStateToProps, mapDispatchToProps)(Container)

export default MainContainer;
