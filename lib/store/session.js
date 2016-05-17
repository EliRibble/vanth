import _ from 'lodash';
import * as Constants from 'vanth/constants';

const emptyState = {
  name      : null,
  username  : null,
  uri       : null,
};

var reducer = function(state = emptyState, action) {
  switch (action.type) {
    case Constants.ActionType.SESSION_GET_COMPLETE:
      return _.assign({}, state, action.data);
    default:
      return state;
  }
}

module.exports = reducer;
