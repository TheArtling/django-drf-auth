import React from "react"
import { createStore, compose, applyMiddleware } from "redux"
import { createEpicMiddleware } from "redux-observable"
import { Provider } from "react-redux"
import { render } from "react-dom"
import { browserHistory, Router, Route } from 'react-router'
import thunk from "redux-thunk"

import { rootEpic } from "./actions/root"
import { rootReducer } from "./reducers"
import AuthContainer from "./containers/AuthContainer"


const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const epicMiddleware = createEpicMiddleware(rootEpic);
export default function configureStore() {
  const store = createStore(
    rootReducer,
    composeEnhancers(
      applyMiddleware(thunk),
      applyMiddleware(epicMiddleware),
    )
  );
  return store;
}
let store = configureStore()


window.fbAsyncInit = function() {
  FB.init({
    appId      : process.env.FACEBOOK_APP_ID,
    cookie     : true,
    xfbml      : true,
    version    : 'v2.8'
  });
}


class AuthApp extends React.Component {
  render() {
    return (
      <Provider store={store}>
        <Router history={browserHistory}>
          <Route path="/" component={AuthContainer} />
          <Route path="/auth/finish-signup/" component={AuthContainer} />
        </Router>
      </Provider>
    )
  }
}


render(<AuthApp />, document.getElementById("authApp"))
