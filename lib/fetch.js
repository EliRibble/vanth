function FetchError(url, status, errors) {
  this.errors   = errors;
  this.message  = `Status code ${status} was returned from ${url}`;
  this.name     = 'FetchError';
  this.status   = status;
  this.url      = url;
}

let _handleResults = function(resolve, reject, url, fetchRequest) {
  fetchRequest
  .then(response => {
    if(response.status == 204) {
      resolve({
        headers : response.headers,
        json    : null,
        text    : '',
      });
    } else if(response.status >= 400) {
      console.error(`The request to ${url} failed with status ${response.status}`, response);
      response.json()
      .then(json => {
        reject(new FetchError(url, response.status, json.errors));
      })
      .catch(reject);
    } else {
      if(response.headers.get('Content-Type') == 'application/json') {
        response.json()
        .then(json => {
          resolve({
            headers : response.headers,
            json    : json,
            text    : null,
          });
        }).catch(reject);
      } else {
        response.text()
        .then(text => {
          resolve({
            headers : response.headers,
            json    : null,
            text    : text,
          });
        }).catch(reject);
      }
    }
  })
  .catch(error => {
    if(error instanceof Error) {
      reject(error);
    } else {
      console.error("Unrecognized error raised when fetching", error);
      reject(new Error("Unknown error occurred during fetch"));
    }
  });
}

export function get(url) {
  return new Promise(function(resolve, reject) {
    _handleResults(resolve, reject, url,
      fetch(url, {
        credentials : 'include',
        method      : 'GET',
      })
    );
  });
}

export function post(url, data) {
  return new Promise(function(resolve, reject) {
    _handleResults(resolve, reject, url,
      fetch(url, {
        credentials : 'include',
        headers     : {
          "Content-Type": "application/json"
        },
        method      : 'POST',
        body        : JSON.stringify(data),
      })
    );
  });
}

export function put(url, data) {
  return new Promise(function(resolve, reject) {
    _handleResults(resolve, reject, url,
      fetch(url, {
        credentials : 'include',
        headers     : {
          "Content-Type": "application/json"
        },
        method      : 'PUT',
        body        : JSON.stringify(data),
      })
    );
  });
}

module.exports.delete = function(url) {
  return new Promise(function(resolve, reject) {
    _handleResults(resolve, reject, url,
      fetch(url, {
        credentials : 'include',
        method      : 'DELETE',
      })
    );
  });
}
