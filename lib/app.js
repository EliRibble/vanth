import { connect, Provider } from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';

import Actions from 'vanth/actions/root';
import RootStore from 'vanth/store/root';
import Routes from 'vanth/routes';

const App = connect(state => state)(React.createClass({
  componentWillMount: function() {
    window.onhashchange = function(event) {
      if(!event) return;
      Actions.URL.change(event.oldURL, event.newURL || window.location.hash);
    }
  },
  render: function() {
    let allProps = _.assign({}, this.props, this.state);
    return (
      <Routes {...allProps}/>
    );
  }
}));

ReactDOM.render((
  <Provider store={RootStore}>
    <App />
  </Provider>
), document.getElementById('container'));

window.onload = function() {
  let thing = Actions.Session.get()
  thing.then(session => {
    console.log(session);
  }).catch(error => {
    //Actions.URL.navigate('/login');
  });
}
module.exports = App;
