var make_constants = function(constants) {
  let result = {};
  for(var i = 0; i < constants.length; i++) {
    let constant = constants[i];
    result[constant] = constant;
  }
  return result;
}

export const ActionType = make_constants([
  'RESOURCE_DELETE',
  'RESOURCE_GET',
  'RESOURCE_POST',
  'RESOURCE_PUT',

  'SESSION_DELETE_BEGIN',
  'SESSION_DELETE_COMPLETE',
  'SESSION_DELETE_ERROR',
  'SESSION_GET_BEGIN',
  'SESSION_GET_COMPLETE',
  'SESSION_GET_ERROR',
  'SESSION_POST_BEGIN',
  'SESSION_POST_COMPLETE',
  'SESSION_POST_ERROR',

  'URL_CHANGE',
  'URL_NAVIGATE',
  'URL_REPLACE',

  'USER_REGISTER_BEGIN',
  'USER_REGISTER_COMPLETE',
  'USER_REGISTER_ERROR',
]);
