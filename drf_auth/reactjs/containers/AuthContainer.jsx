import React from "react"
import Radium from "radium"
import { connect } from "react-redux"

import LoginForm from "../components/LoginForm"
import SignupForm from "../components/SignupForm"


const styles = {
  base: {

  }
}


@connect(state => ({
  currentForm: state.auth.currentForm,
}))
@Radium
export default class AuthContainer extends React.Component {
  render() {
    let { currentForm } = this.props

    return (
      <div>
        {(currentForm == 'login') &&
          <LoginForm />
        }
        {(currentForm == 'signup') &&
          <SignupForm />
        }
      </div>
    )
  }
}
