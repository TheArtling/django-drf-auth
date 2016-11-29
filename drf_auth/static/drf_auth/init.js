var drfAuthLoginClick = new CustomEvent('drfAuthLoginClick');
var drfAuthSignupClick = new CustomEvent('drfAuthSignupClick');
var drfAuthPasswordForgottenClick = new CustomEvent('drfAuthPasswordForgottenClick');
function drfAuthLoginClicked() { window.dispatchEvent(drfAuthLoginClick); }
function drfAuthSignupClicked() { window.dispatchEvent(drfAuthSignupClick); }
function drfAuthPasswordForgottenClicked() { window.dispatchEvent(drfAuthPasswordForgottenClick); }
