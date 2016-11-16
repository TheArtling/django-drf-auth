import "rxjs/add/observable/of";
import { ajax } from "rxjs/observable/dom/ajax"
import { catch } from "rxjs/add/operator/catch"
import { Observable } from "rxjs/Observable"
import cookie from "react-cookie"
import debounceTime from "rxjs/add/operator/debounceTime"
import map from "rxjs/add/operator/map"
import mergeMap from "rxjs/add/operator/mergeMap"


export const AJAX_REQUEST = "AJAX_REQUEST"
export const AJAX_FULFILLED = "AJAX_FULFILLED"
export const AJAX_REJECTED = "AJAX_REJECTED"
export function ajaxEpicFactory(TYPE, urlFunc, method) {
  return (action$, store) => {
    return action$.ofType(TYPE).
      mergeMap(action => {
        let url = urlFunc(action)
        let headers = {
          "X-CSRFToken": cookie.load("csrftoken"),
          "Content-Type": "application/json",
          "Accept": "application/json",
        }
        let options = {
          url: url,
          headers: headers,
          withCredentials: true,
          crossDomain: true,
          responseType: "json",
          method: method,
        }
        if(action.formValues) {
          if (options.method === "PATCH" ||
              options.method === "POST" ||
              options.method === "PUT") {
            options.body = action.formValues
          }
          if (options.method === "GET") {
            console.log("UNEXPECTED ACTION!");
            // TODO: if needed, import url-query-utils
            //options.url += getQuery(action.formValues)
          }
        }
        store.dispatch({type: AJAX_REQUEST, action: TYPE, options: options})
        return ajax(options)
          .map(
            (response, status) => {
              let success = {
                type: AJAX_FULFILLED,
                action: TYPE,
                payload: {
                  response: response,
                  status: status
                }
              }
              if (action.successCallback) { action.successCallback(success) }
              return success
            }
          )
          .catch(error => {
            return Observable.of({
              type: AJAX_REJECTED,
              payload: error,
              action: TYPE,
              error: true
            })
          })
        }
      )
  }
}
