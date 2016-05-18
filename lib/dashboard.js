import * as BS from 'react-bootstrap';
import React from 'react';

import * as Actions from 'vanth/actions/root';
import Navbar from 'vanth/navbar';

var Dashboard = React.createClass({
  logout: function() {
    Actions.Session.logout(this.props.session.uri).then(() => {
      Actions.URL.navigate('/login');
    });
  },
  render: function() {
    return (
      <div className='container-fluid'>
        <Navbar/>
        <p>Welcome home</p>
      </div>
    );
  }
});

module.exports = Dashboard
