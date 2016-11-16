import { ajaxEpicFactory } from "./utils"


export const SET_CURRENT_FORM = "SET_CURRENT_FORM"
export const setCurrentForm = (form) => ({type: SET_CURRENT_FORM, form: form})


export const POST_LOGIN = "POST_LOGIN"
export const postLogin = (formValues, successCallback) => ({
  type: POST_LOGIN, formValues: formValues, successCallback: successCallback })
export const postLoginEpic = ajaxEpicFactory(
  POST_LOGIN, (action) => "/api/v1/login/", "POST",
)


export const POST_FB_LOGIN = "POST_FB_LOGIN"
export const postFacebookLogin = (formValues, successCallback) => ({
  type: POST_FB_LOGIN, formValues: formValues, successCallback: successCallback })
export const postFacebookLoginEpic = ajaxEpicFactory(
  POST_FB_LOGIN, (action) => "/api/v1/fb-login/", "POST",
)
