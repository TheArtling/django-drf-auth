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
        <div onClick={() => this.handleSignup()}>Go to Signup</div>
      </div>
    )
  }
}
