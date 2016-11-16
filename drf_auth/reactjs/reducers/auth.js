import * as auth from "../actions/auth"


const initialState = {
  currentForm: "login",
}


export default function reducer(state=initialState, action={}) {
  switch (action.type) {
  case auth.SET_CURRENT_FORM:
    return { ...state, currentForm: action.form }
  default:
    return state
  }
}
