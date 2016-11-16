import { combineReducers } from "redux"
import { default as accounts } from "./accounts"
import { default as auth } from "./auth"


export const rootReducer = combineReducers({
  accounts,
  auth,
});
