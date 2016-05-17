import * as ActionTools from 'vanth/actions/tools';

export function createSession(username, password, nextPath=null) {
  const payload = {
    password: password,
    username: username,
  };
  return ActionTools.fetchAndDispatch(
    '/session/',
    'SESSION_POST_BEGIN',
    'SESSION_POST_COMPLETE',
    'SESSION_POST_ERROR',
    ActionTools.Methods.POST,
    payload,
  );
}

export function get() {
  return ActionTools.fetchAndDispatch(
    '/session/',
    'SESSION_GET_BEGIN',
    'SESSION_GET_COMPLETE',
    'SESSION_GET_ERROR'
  );
}

export function logout(uri) {
  return ActionTools.fetchAndDispatch(
    uri,
    'SESSION_DELETE_BEGIN',
    'SESSION_DELETE_COMPLETE',
    'SESSION_DELETE_ERROR',
    ActionTools.Methods.DELETE,
  );
}
