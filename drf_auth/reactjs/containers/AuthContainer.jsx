import React from 'react'
import Radium from 'radium'
import { connect } from 'react-redux'

import * as authActions from '../actions/auth'
import LoginForm from '../components/LoginForm'
import SignupForm from '../components/SignupForm'


const styles = {
  base: {
    background: '#AFAFAF',
    height: '0px',
    overflow: 'hidden',
    transition: 'height 0.5s',
  },
  isVisible: {
    height: '100px',
  }
}


@connect(state => ({
  currentForm: state.auth.currentForm,
}))
@Radium
export default class AuthContainer extends React.Component {
  constructor(props) {
    super(props)
    this.state = { isVisible: false }
  }

  componentDidMount() {
    window.addEventListener(
      'drfAuthLoginClick', () => this.handleLoginClick())
    window.addEventListener(
      'drfAuthSignupClick', () => this.handleSignupClick())
    window.addEventListener(
      'drfAuthPasswordForgottenClick',
      () => this.handlePasswordForgottenClick())
  }

  componentWillUnmount() {
    window.removeEventListener(
      'drfAuthLoginClick', () => this.handleLoginClick())
    window.removeEventListener(
      'drfAuthSignupClick', () => this.handleSignupClick())
    window.removeEventListener(
      'drfAuthPasswordForgottenClick',
      () => this.handlePasswordForgottenClick())
  }

  handleLoginClick() { this.toggleState('login') }
  handleSignupClick() { this.toggleState('signup') }
  handlePasswordForgottenClick() { this.toggleState('passwordForgotten') }

  toggleState(newForm) {
    let { currentForm, dispatch } = this.props
    if (currentForm == newForm) {
      this.setState({isVisible: !this.state.isVisible})
    } else {
      this.setState({isVisible: true})
      dispatch(authActions.setCurrentForm(newForm))
    }
  }

  render() {
    let { currentForm } = this.props
    let { isVisible, view } = this.state

    return (
      <div style={[
        styles.base,
        isVisible && styles.isVisible,
      ]}>
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
