import {makePostCall, makeGetCall, makePutCall} from "./ajax";

function selectLogin() {
    return {
        type: "SELECT_LOGIN"
    }
}

function selectSignup() {
    return {
        type: "SELECT_SIGNUP"
    }
}

function selectMyOrders() {
    return {
        type: "SELECT_MY_ORDERS"
    }
}

function selectRestaurantOrders() {
    return {
        type: "SELECT_RESTAURANT_ORDERS"
    }
}

function selectProfile() {
    return {
        type: "SELECT_PROFILE"
    }
}

function loginRequested() {
    return {
        type: "LOGIN_REQUESTED"
    }
}

function loginSuccessful(user) {
    return {
        type: "LOGIN_SUCCESSFUL",
        user: user
    }
}

function loginFailed(error) {
    return {
        type: "LOGIN_FAILED",
        error: error
    }
}

function updateUserSuccessful(user) {
    return {
        type: "UPDATE_USER_SUCCESSFUL",
        user: user
    }
}

function updateUserFailed(error) {
    return {
        type: "UPDATE_USER_FAILED",
        error: error
    }
}

function logoutSuccessful() {
    return {
        type: "LOGOUT_SUCCESSFUL"
    }
}

function logoutFailed(error) {
    return {
        type: "LOGOUT_FAILED",
        error: error
    }
}

function  doLogin(username, password) {
    return function(dispatch) {
        dispatch(loginRequested);
        makePostCall(
          "api/v1/users/authenticated",
          {
            username: username,
            password: password
          }
        ).then(user => dispatch(loginSuccessful(user))
          ).catch(res => dispatch(loginFailed(res)));
    }
}

function doLogout() {
    return function(dispatch) {
        makePostCall("api/v1/users/logout")
          .then(res => {dispatch(logoutSuccessful()), dispatch(selectLogin())})
          .fail(res => dispatch(logoutFailedf(error)));
    }
}

function signupSuccessful() {
    return {
        type: "SIGNUP_SUCCESSFUL"
    }
}

function signupFailed(error) {
    return {
        type: "SIGNUP_FAILED",
        error: error
    }
}

function doSignup(username, password, firstname, lastname, email, restaurantOwner) {
    return function(dispatch) {
        makePostCall("api/v1/users/signup",
            {
                username: username,
                firstname: firstname,
                lastname: lastname,
                password: password,
                email: email,
                restaurant_owner: restaurantOwner
            }
        ).then(res => {dispatch(signupSuccessful), dispatch(selectLogin())})
         .fail(err => dispatch(signupFailed));
    }
}

function checkAuthenticated() {
    return function(dispatch) {
        makeGetCall("api/v1/users/authenticated")
          .done(user => dispatch(loginSuccessful(user)));
    }
}

function updateUser(userId, firstname, lastname) {
    return function(dispatch) {
        makePutCall("api/v1/users/" + userId, {firstname: firstname, lastname: lastname})
          .done(user => dispatch(updateUserSuccessful(user)))
          .fail(res => dispatch(updateUserFailed(res)));
    }
}

function requestedRestaurants() {
    return {
        type: "REQUESTED_RESTAURANTS"
    }
}

function requestedOwnerRestaurants() {
    return {
        type: "REQUESTED_OWNER_RESTAURANTS"
    }
}

function receivedRestaurants(restaurants) {
    return {
        type: "RECEIVED_RESTAURANTS",
        restaurants: restaurants
    }
}

function failedToReceiveRestaurants(error) {
    return {
        type: "FAILED_TO_RECEIVE_RESTAURANTS",
        error: error
    }
}

function failedToReceiveOwnerRestaurants(error) {
    return {
        type: "FAILED_TO_RECEIVE_OWNER_RESTAURANTS",
        error: error
    }
}

function receivedOwnerRestaurants(restaurants) {
    return {
        type: "RECEIVED_OWNER_RESTAURANTS",
        restaurants: restaurants
    }
}

function selectRestaurants() {
    return function(dispatch) {
        dispatch(requestedRestaurants);
        makeGetCall("api/v1/restaurants")
          .done(restaurants => dispatch(receivedRestaurants(restaurants)))
          .fail(res => dispatch(failedToReceiveRestaurants(restaurants)));
    }
}

function selectOwnerRestaurants(ownerId) {
    return function(dispatch) {
        dispatch(requestedOwnerRestaurants);
        makeGetCall("api/v1/users/" + ownerId + "/restaurants")
          .done(restaurants => dispatch(receivedOwnerRestaurants(restaurants)))
          .fail(err => dispatch(failedToReceiveOwnerRestaurants(err)))
    }
}

function requestedCreateRestaurant() {
    return {
        type: "REQUESTED_CREATE_RESTAURANT"
    }
}

function failedToCreateRestaurant(error) {
    return {
        type: "FAILED_TO_CREATE_RESTAURANT",
        error: error
    }
}

function createRestaurant(name, description) {
    return function(dispatch) {
        dispatch(requestedCreateRestaurant);
        makePostCall("api/v1/restaurants", {name: name, description: description})
          .done(restaurant => dispatch(selectOwnerRestaurants(restaurant.owner_id)))
          .fail(err => dispatch(failedToCreateRestaurant));
    }
}

function requestedCreateMeal() {
    return {
        type: "REQUESTED_CREATE_MEAL"
    }
}

function mealCreated(meal) {
    return {
        type: "MEAL_CREATED",
        meal: meal
    }
}

function failedToCreateMeal(error) {
    return {
        type: "FAILED_TO_CREATE_MEAL",
        error: error
    }
}

function createRestaurantMeal(restaurant_id, name, description, price) {
    return function(dispatch) {
        dispatch(requestedCreateMeal);
        makePostCall("api/v1/restaurants/" + restaurant_id + "/meals", {name: name, description: description, price: parseFloat(price)})
          .done(meal => dispatch(mealCreated(meal)))
          .fail(err => dispatch(failedToCreateMeal(err)));
    }
}

function addMealToOrder(meal) {
    return {
        type: "ADD_MEAL_TO_ORDER",
        meal: meal
    }
}

function requestGetMyOrders() {
    return {
        type: "REQUEST_MY_ORDERS"
    }
}

function requestMyOrdersSucceeded(orders) {
    return {
        type: "REQUEST_MY_ORDERS_SUCCEEDED",
        orders: orders
    }
}

function requestMyOrdersFailed(error) {
    return {
        type: "REQUEST_MY_ORDERS_FAILED",
        error: error
    }
}

function getMyOrders(userId) {
    return function(dispatch) {
        dispatch(requestGetMyOrders);
        makeGetCall("api/v1/users/" + userId + "/orders")
          .done(orders => {dispatch(requestMyOrdersSucceeded(orders))})
          .fail(error => dispatch(requestMyOrdersFailed(error)));
    }
}

function requestPlaceOrder() {
    return {
        type: "REQUEST_PLACE_ORDER"
    }
}

function orderPlacementSucceeded(order) {
    return {
        type: "ORDER_PLACEMENT_SUCCEEDED",
        order: order
    }
}

function orderPlacementFailed(error) {
    return {
        type: "ORDER_PLACEMENT_FAILED",
        error: error
    }
}

function placeOrder(userId, restaurantId, unplacedOrderData) {
    return function(dispatch) {
        dispatch(requestPlaceOrder);
        makePostCall("api/v1/restaurants/" + restaurantId + "/orders", {meal_ids: Object.keys(unplacedOrderData)})
          .done(order => {dispatch(orderPlacementSucceeded(order)),dispatch(getMyOrders(userId))})
          .fail(error => dispatch(orderPlacementFailed(error)));
    }
}

function cancelUnplacedOrder(restaurantId) {
    return {
        type: "CANCEL_UNPLACED_ORDER",
        restaurantId: restaurantId
    }
}


function requestGetIncomingOrders() {
    return {
        type: "REQUEST_INCOMING_ORDERS"
    }
}

function requestIncomingOrdersSucceeded(orders) {
    return {
        type: "REQUEST_INCOMING_ORDERS_SUCCEEDED",
        orders: orders
    }
}

function requestIncomingOrdersFailed(error) {
    return {
        type: "REQUEST_INCOMING_ORDERS_FAILED",
        error: error
    }
}

function getIncomingOrders(userId) {
    return function(dispatch) {
        dispatch(requestGetIncomingOrders);
        makeGetCall("api/v1/users/" + userId + "/incoming_orders")
          .done(orders => {dispatch(requestIncomingOrdersSucceeded(orders))})
          .fail(error => dispatch(requestIncomingOrdersFailed(error)));
    }
}

function requestIncrementMyOrder() {
    return {
        type: "REQUEST_INCREMENT_MY_ORDER"
    }
}

function requestIncrementMyOrderSucceeded(order) {
    return {
        type: "REQUEST_INCREMENT_MY_ORDER_SUCCEEDED",
        order: order
    }
}

function requestIncrementMyOrderFailed(error) {
    return {
        type: "REQUEST_INCREMENT_MY_ORDER_FAILED",
        error: error
    }
}

function incrementMyOrderStatus(userId, orderId) {
    return function(dispatch) {
        dispatch(requestIncrementMyOrder);
        makePutCall("api/v1/users/" + userId + "/orders/" + orderId + "/increment_status", {})
          .done(order => {dispatch(requestIncrementMyOrderSucceeded(order))})
          .fail(error => dispatch(requestIncrementMyOrderFailed(error)));
    }
}

function requestIncrementIncomingOrder() {
    return {
        type: "REQUEST_INCREMENT_INCOMING_ORDER"
    }
}

function requestIncrementIncomingOrderSucceeded(order) {
    return {
        type: "REQUEST_INCREMENT_INCOMING_ORDER_SUCCEEDED",
        order: order
    }
}

function requestIncrementIncomingOrderFailed(error) {
    return {
        type: "REQUEST_INCREMENT_INCOMING_ORDER_FAILED",
        error: error
    }
}

function incrementIncomingOrderStatus(userId, orderId) {
    return function(dispatch) {
        dispatch(requestIncrementMyOrder);
        makePutCall("api/v1/users/" + userId + "/incoming_orders/" + orderId + "/increment_status", {})
          .done(order => {dispatch(requestIncrementIncomingOrderSucceeded(order))})
          .fail(error => dispatch(requestIncrementIncomingOrderFailed(error)));
    }
}

export {
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
    };
