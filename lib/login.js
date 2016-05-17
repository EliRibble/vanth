import React                    from 'react';
import * as BS                  from 'react-bootstrap';
import { bindActionCreators }   from 'redux';

import Actions                  from 'vanth/actions/root';

module.exports = React.createClass({
  getInitialState() {
    return {
      password  : null,
      username  : null,
    }
  },

  handleChange: function(parameter) {
    return (e) => {
      this.setState({
        [parameter] : e.target.value
      });
    }
  },

  handleSubmit: function(e) {
    e.preventDefault();

    Actions.Session.createSession(
      this.state.username,
      this.state.password,
      this.props.url.search.nextPath || "/"
    ).then(result => {
      Actions.Session.get();
      Actions.URL.navigate('/');
    }).catch(error => {
      console.error(error);
    });
  },

  render: function() {
    const forgotPassword = <a href="#/forgot" className="pull-right"><small>Forgot Password</small></a>;
    const pending = false;
    return (
      <BS.Grid>
        <BS.Row>
          <BS.Col xs={8} xsOffset={2}>
            <h3 className="primary">Login</h3>
            <hr />
            <form onSubmit={this.handleSubmit} className='form-horizontal'>
              <BS.FormGroup controlId="login">
                <BS.ControlLabel>Username</BS.ControlLabel>
                <BS.FormControl
                  disabled={pending}
                  onChange={this.handleChange('username')}
                  placeholder='Username'
                  required
                  type='text'
                  wrapperClassName='col-xs-10'
                />
                <BS.ControlLabel>Password</BS.ControlLabel>
                <BS.FormControl
                  disabled={pending}
                  onChange={this.handleChange('password')}
                  placeholder='Password'
                  required
                  type='password'
                  wrapperClassName='col-xs-10'
                />
                <BS.Button bsStyle='primary' type='submit' className='col-xs-3 col-xs-offset-2' disabled={pending}>Login</BS.Button>
                <BS.Button bsStyle='link' className='col-xs-1' href="#/register">Register</BS.Button>
              </BS.FormGroup>
            </form>
          </BS.Col>
        </BS.Row>
      </BS.Grid>
    );
  }
});
