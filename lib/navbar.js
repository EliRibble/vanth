import * as BS from 'react-bootstrap';
import React from 'react';

module.exports = React.createClass({
  render: function() {
    return (
      <BS.Navbar>
        <BS.Navbar.Header>
          <BS.Navbar.Brand>
            <a href="/">Vanth</a>
          </BS.Navbar.Brand>
        </BS.Navbar.Header>
        <BS.Nav>
          <BS.NavItem eventKey={1} href="#/accounts">Accounts</BS.NavItem>
          <BS.NavDropdown eventKey={2} title="Account" id="account">
            <BS.MenuItem eventKey={2.1} onClick={this.logout}>Logout</BS.MenuItem>
          </BS.NavDropdown>
        </BS.Nav>
      </BS.Navbar>
    );
  }
});
