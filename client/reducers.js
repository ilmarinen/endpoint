// const initialState = {
//     selectedTab: "LOGIN",
//     tabStatus: "LOADED",
//     unplacedOrders: {},
//     orders: [],
//     restaurantOrders: [],
//     restaurants: [],
//     ownerRestaurants: [],
//     session: {
//         authenticated: false,
//         user: null
//     },
//     errorMessage: null
// }
const initialState = window.APP_STATE;

function rootReducer(state = initialState, action) {
    switch(action.type) {
        case "SELECT_LOGIN":
            return Object.assign({}, state, {selectedTab: "LOGIN"});
        case "SELECT_SIGNUP":
            return Object.assign({}, state, {selectedTab: "SIGNUP"});
        case "SELECT_MY_ORDERS":
            return Object.assign({}, state, {selectedTab: "MY_ORDERS"});
        // case "SELECT_RESTAURANT_ORDERS":
        //     return Object.assign({}, state, {selectedTab: "RESTAURANT_ORDERS"});
        case "SELECT_PROFILE":
            return Object.assign({}, state, {selectedTab: "PROFILE"});
        case "LOGIN_REQUESTED":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "LOGIN_SUCCESSFUL":
            return Object.assign({}, state, {selectedTab: "PROFILE", tabStatus: "LOADED", session: {authenticated: true, user: action.user}});
        case "LOGIN_ERROR":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Login failed"});
        case "UPDATE_USER_SUCCESSFUL":
            return Object.assign({}, state, {selectedTab: "PROFILE", session: {authenticated: true, user: action.user}});
        case "UPDATE_USER_FAILED":
            return Object.assign({}, state, {errorMessage: "Update user failed"});
        case "LOGOUT_SUCCESSFUL":
            return Object.assign({}, state, {selectedTab: "LOGIN", session: {authenticated: false, user: null}});
        case "LOGOUT_FAILED":
            return Object.assign({}, state, {selectedTab: "PROFILE", errorMessage: "Logout failed"})
        case "SIGNUP_SUCCESSFUL":
            return Object.assign({}, state, {selectedTab: "PROFILE"});
        case "SIGNUP_FAILED":
            return Object.assign({}, state, {selectedTab: "PROFILE", errorMessage: "Signup failed"});
        case "REQUESTED_RESTAURANTS":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUESTED_OWNER_RESTAURANTS":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "RECEIVED_RESTAURANTS":
            return Object.assign({}, state, {tabStatus: "LOADED", selectedTab: "RESTAURANTS", restaurants: action.restaurants});
        case "RECEIVED_OWNER_RESTAURANTS":
            return Object.assign({}, state, {tabStatus: "LOADED", selectedTab: "OWNER_RESTAURANTS", ownerRestaurants: action.restaurants});
        case "FAILED_TO_RECEIVE_RESTAURANTS":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to receive restaurants"});
        case "FAILED_TO_RECEIVE_OWNER_RESTAURANTS":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to receive owner restaurants"});
        case "REQUESTED_CREATE_MEAL":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "MEAL_CREATED":
            let restaurants
            restaurants = state.ownerRestaurants.map(restaurant => {
                if (action.meal.restaurant_id == restaurant.id) {
                    restaurant.meals.push(action.meal);
                }
                return restaurant;
            });
            return Object.assign({}, state, {tabStatus: "LOADED", ownerRestaurants: restaurants});
        case "FAILED_TO_CREATE_MEAL":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to create meal"});
        case "ADD_MEAL_TO_ORDER":
            let unplacedOrders = state.unplacedOrders;
            let unplacedOrdersForRestaurant = unplacedOrders[action.meal.restaurant_id] || {};
            unplacedOrdersForRestaurant[action.meal.id] = action.meal;
            unplacedOrders[action.meal.restaurant_id] = unplacedOrdersForRestaurant
            return Object.assign({}, state, {unplacedOrders: unplacedOrders});
        case "ORDER_PLACEMENT_SUCCEEDED":
            let unplacedOrdersAfterPlaced = state.unplacedOrders;
            delete unplacedOrdersAfterPlaced[action.order.restaurant_id];
            return Object.assign({}, state, {tabStatus: "LOADED", unplacedOrders: unplacedOrdersAfterPlaced});
        case "REQUEST_PLACE_ORDER":
            console.log("request place order");
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "ORDER_PLACEMENT_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to place order"});
        case "CANCEL_UNPLACED_ORDER":
            let unplacedOrdersWithCancel = state.unplacedOrders;
            delete unplacedOrdersWithCancel[action.restaurantId];
            return Object.assign({}, state, {unplacedOrders: unplacedOrdersWithCancel});
        case "REQUEST_MY_ORDERS":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUEST_MY_ORDERS_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to load orders"});
        case "REQUEST_MY_ORDERS_SUCCEEDED":
            return Object.assign({}, state, {tabStatus: "LOADED", selectedTab: "MY_ORDERS", orders: action.orders});
        case "REQUEST_INCOMING_ORDERS":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUEST_INCOMING_ORDERS_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to load incoming orders"});
        case "REQUEST_INCOMING_ORDERS_SUCCEEDED":
            return Object.assign({}, state, {tabStatus: "LOADED", selectedTab: "RESTAURANT_ORDERS", restaurantOrders: action.orders});
        case "REQUEST_INCREMENT_MY_ORDER":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUEST_INCREMENT_MY_ORDER_SUCCEEDED":
            let updatedMyOrders = [];
            state.orders.forEach(order => {
                if (order.id == action.order.id) {
                    updatedMyOrders.push(action.order);
                } else {
                    updatedMyOrders.push(order);
                }
            });
            return Object.assign({}, state, {tabStatus: "LOADED", selectedTab: "MY_ORDERS", orders: updatedMyOrders});
        case "REQUEST_INCREMENT_MY_ORDER_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to update order status"});

        case "REQUEST_INCREMENT_INCOMING_ORDER":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUEST_INCREMENT_INCOMING_ORDER_SUCCEEDED":
            let updatedIncomingOrders = [];
            state.restaurantOrders.forEach(order => {
                if (order.id == action.order.id) {
                    updatedIncomingOrders.push(action.order);
                } else {
                    updatedIncomingOrders.push(order);
                }
            });
            return Object.assign({}, state, {tabStatus: "LOADED", selectedTab: "RESTAURANT_ORDERS", restaurantOrders: updatedIncomingOrders});
        case "REQUEST_INCREMENT_INCOMING_ORDER_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to update order status"});
        default:
            return state
    }
}

export default rootReducer;
