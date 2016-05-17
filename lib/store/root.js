import { combineReducers }        from 'redux';
import createStoreWithMiddleware  from 'vanth/middleware';

import SessionReducer             from 'vanth/store/session';
import URLReducer                 from 'vanth/store/url';

const root = combineReducers({
  session : SessionReducer,
  url     : URLReducer,
});

const store = createStoreWithMiddleware(root);

module.exports = store;
