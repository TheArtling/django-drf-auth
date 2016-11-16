import { combineEpics } from "redux-observable"
import * as auth from "./auth"


export const rootEpic = combineEpics(
  auth.postLoginEpic,
)
