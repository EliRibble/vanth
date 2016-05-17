import { applyMiddleware, createStore } from 'redux';

import thunkMiddleware  from 'redux-thunk';
import createLogger     from 'redux-logger';

const loggerMiddleware = createLogger();
var createStoreWithMiddleware = applyMiddleware(
    thunkMiddleware, // lets us dispatch() functions
    loggerMiddleware // neat middleware that logs actions
)(createStore);

module.exports = createStoreWithMiddleware;
