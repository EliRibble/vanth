import * as ActionTools from 'vanth/actions/tools';

export function register(name, username, password) {
  const payload = {
    name    : name,
    password: password,
    username: username,
  }
  return ActionTools.fetchAndDispatch(
    '/user/',
    'USER_REGISTER_BEGIN',
    'USER_REGISTER_COMPLETE',
    'USER_REGISTER_ERROR',
    ActionTools.Methods.POST,
    payload
  );
}
