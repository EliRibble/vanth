import _              from 'lodash';

import Config           from 'vanth/config';
import { ActionType }   from 'vanth/constants';
import * as Fetch       from 'vanth/fetch';

export const Methods = {
  DELETE : 'delete',
  GET    : 'get',
  PATCH  : 'patch',
  POST   : 'post',
  PUT    : 'put',
}

export function action(type) {
  return function(data) {
    let action = {
      type: ActionType[type],
    }
    if(data != undefined) {
      action.data = data;
    }
    if(!action.type) {
      throw new Error(`An action type is required.  Could not find an action type constant for ${type}`);
    }
    return action;
  }
}

export function ensureConstantAction(constant) {
  if(typeof constant === "string") {
    if(!ActionType[constant]) {
      let message = `${constant} is not a valid constant - you'll need to add it to constants.js`;
      console.error(message)
      throw new Error(message);
    }
    return action(constant);
  }
  return constant;
}

export function fetchAndDispatch(url, start, end, failed, method=Methods.GET, payload) {
  let actionStart = ensureConstantAction(start);
  let actionEnd = ensureConstantAction(end);
  let actionFailed = ensureConstantAction(failed);

  if(!Fetch[method]) {
    throw new Error(`Invalid method for fetcher: ${method}`);
  }

  if(!payload && (method === Methods.POST || method === Methods.PUT)) {
    throw new Error(`A payload is required for a ${method} method`);
  }

  let actionData = {};
  if(method === Methods.PUT || method === Methods.DELETE) {
    actionData.uri = url;
  } else {
    actionData.url = url;
  }

  return dispatch => {
    dispatch(actionStart(actionData));
    let fullURL = url.indexOf('://') >= 0 ? url : Config.API + url;
    return Fetch[method].call(this, fullURL, payload)
    .then(response => {
      let result = response.json;
      switch(method) {
        case Methods.GET:
          break;
        case Methods.POST:
          result = _.assign({}, payload, {
            uri: response.headers.get('Location')
          }, actionData);
          break;
        case Methods.PUT:
          result = _.assign({}, payload, {
            uri: url
          });
          break;
        case Methods.DELETE:
          result = actionData;
          break;
      }
      let eventType = {
        [Methods.DELETE]  : 'RESOURCE_DELETE',
        [Methods.GET]     : 'RESOURCE_GET',
        [Methods.PUT]     : 'RESOURCE_PUT',
        [Methods.POST]    : 'RESOURCE_POST',
      }[method];
      dispatch(ensureConstantAction(eventType)(result));
      dispatch(actionEnd(result));
      return result;
    })
    .catch(data => {
      actionData.errors = data.errors ? data.errors : [data];
      dispatch(actionFailed(actionData));
      throw data;
    });
  }
}

