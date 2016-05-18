import * as BS from 'react-bootstrap';
import React from 'react';

import Navbar from 'vanth/navbar';
module.exports = React.createClass({
  render: function() {
    return (
      <div className='container-fluid'>
        <Navbar/>
        <p>You don't have any accounts yet!</p>
      </div>
    );
  }
});
