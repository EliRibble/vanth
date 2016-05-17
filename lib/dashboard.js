import * as BS from 'react-bootstrap';
import React from 'react';

import * as Actions from 'vanth/actions/root';

var Dashboard = React.createClass({
  logout: function() {
    Actions.Session.logout(this.props.session.uri).then(() => {
      Actions.URL.navigate('/login');
    });
  },
  render: function() {
    return (
      <div className='container-fluid'>
        <BS.Navbar>
          <BS.Navbar.Header>
            <BS.Navbar.Brand>
              <a href="/">Vanth</a>
            </BS.Navbar.Brand>
          </BS.Navbar.Header>
          <BS.Nav>
            <BS.NavItem eventKey={1} href="/thing">Thing</BS.NavItem>
            <BS.NavDropdown eventKey={2} title="Account" id="account">
              <BS.MenuItem eventKey={2.1} onClick={this.logout}>Logout</BS.MenuItem>
            </BS.NavDropdown>
          </BS.Nav>
        </BS.Navbar>
      </div>
    );
  }
});

module.exports = Dashboard
