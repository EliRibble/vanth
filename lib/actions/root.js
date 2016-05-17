import { bindActionCreators } from 'redux';

import * as ActionsSession    from 'vanth/actions/session';
import * as ActionsURL        from 'vanth/actions/url';
import * as ActionsUser       from 'vanth/actions/user';

import RootStore              from 'vanth/store/root';

module.exports = {
  Session  : bindActionCreators(ActionsSession, RootStore.dispatch),
  URL      : bindActionCreators(ActionsURL,     RootStore.dispatch),
  User     : bindActionCreators(ActionsUser,    RootStore.dispatch),
}
