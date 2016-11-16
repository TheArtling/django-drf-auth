import React from "react"
import Radium from "radium"
import { connect } from "react-redux"

import * as auth from "../actions/auth"


const styles = {
  base: {

  }
}

@connect(state => ({}))
@Radium
export default class LoginForm extends React.Component {
  componentDidMount() {
    (function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
  }

  handleFBLoginCallback(resp) {
    this.props.dispatch(
      auth.postFacebookLogin(resp, () => this.handleSubmitSuccess()))
  }

  handleFBLogin() {
    FB.login(
      (resp) => this.handleFBLoginCallback(resp),
      {scope: 'email'}
    );
  }

  handleSignup() {
    this.props.dispatch(auth.setCurrentForm('signup'))
  }

  handleSubmitSuccess() {
    location.reload()
  }

  handleSubmit(e) {
    e.preventDefault()
    let formValues = {
      email: this.form.email.value,
      password: this.form.password.value,
    }
    this.props.dispatch(
      auth.postLogin(formValues, () => this.handleSubmitSuccess()))
  }

  render() {
    return (
      <div>
        <form
          ref={(ref) => this.form = ref}
          onSubmit={(e) => this.handleSubmit(e)}
        >
          <input type="text" name="email" />
          <input type="password" name="password" />
          <button type="submit">Login</button>
        </form>
        <div onClick={() => this.handleFBLogin()}>Login with Facebook</div>
        <div onClick={() => this.handleSignup()}>Go to Signup</div>
      </div>
    )
  }
}
