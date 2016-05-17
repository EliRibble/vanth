import { ActionType }     from 'vanth/constants';

export function change(oldURL, newURL) {
  return {
    type  : ActionType.URL_CHANGE,
    data  : {
      oldURL  : oldURL,
      newURL  : newURL,
    }
  }
}

export function replace(newURL) {
  let oldURL = window.location.href;
  history.replaceState(null, '', '#' + newURL);
  return change(oldURL, window.location.href);
}

export function navigate(newURL, query) {
  let oldURL = window.location.href;
  let url = '#' + newURL;
  if(query) {
    url = "?nextPath=" + query + url;
  } else {
    url = "/" + url;
  }
  history.pushState(null, '', url);
  return change(oldURL, window.location.href);
}
