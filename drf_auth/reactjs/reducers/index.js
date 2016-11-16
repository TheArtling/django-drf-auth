import { combineReducers } from "redux"
import { default as accounts } from "./accounts"


export const rootReducer = combineReducers({
  accounts,
});
