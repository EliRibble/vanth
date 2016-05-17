import urllite        from 'urllite';

import { ActionType } from 'vanth/constants';

let _parseSearch = function(location) {
  let search = {};
  let query = location.search.substring(1);
  let vars = query.split('&');
  for(var i = 0; i < vars.length; i++) {
    var pair = vars[i].split('=');
    search[pair[0]] = decodeURIComponent(pair[1]);
  }
  return search;
}

const initialState = {
  location  : urllite(window.location),
  search    : _parseSearch(urllite(window.location)),
};

var reducer = function(state = initialState, action) {
  switch (action.type) {
    case ActionType.URL_CHANGE:
      let location = urllite(action.data.newURL);
      return _.assign({}, state, {
        location: location,
        search: _parseSearch(location)
      });
    default:
      return state;
  }
}

module.exports = reducer;
