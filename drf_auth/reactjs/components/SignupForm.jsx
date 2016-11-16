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
export default class SignupForm extends React.Component {
  handleLogin() {
    this.props.dispatch(auth.setCurrentForm('login'))
  }

  render() {
    return (
      <div>
        Signup
        <div onClick={() => this.handleLogin()}>Go to Login</div>
      </div>
    )
  }
}
