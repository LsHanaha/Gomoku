/* eslint-disable react/jsx-props-no-spreading */
/* eslint-disable react/prop-types */

import "./App.scss";

import React from 'react';
import { useEffect, useState } from "react";
import { Switch, Route, Redirect, BrowserRouter } from "react-router-dom";

import { ROUTER_ENDPOINTS } from "services/constants";

import {NotFound} from "./features/notFound/notFound";

import { GreetingsPage } from "features/greetings/GreetingPage";
import { SignInPage } from "features/signIn/SignInPage";
import { SignUpPage } from "features/signUp/SignUpPage";
import { RestorePwdPage } from "features/restorePwdPage/RestorePasswordPage";
import { RestorePwdMailPage } from "features/restorePwdMail/RestorePasswordMailPage";
import { VerifyEmailPage } from "features/emailVerification/EmailVerificationPage";
import { HomePage } from "features/home/HomePage";
import { NewGame } from "features/newGame/newGame";
import { Game } from "features/game/game";

import checkAuthentication from "services/auth/checkAuthentication";
// import 'bootstrap/dist/css/bootstrap.min.css';

// import history from 'services/history';

function App() {
  const [isUserLoggedIn, setUserLoggedIn] = useState(false);
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthentication()
      .then((user) => {
        setUserLoggedIn(user?.status);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="App">
      {isLoading ? (
        <div>Loading</div>
      ) : (
        <BrowserRouter>
          <Switch>
            <Route
              path={ROUTER_ENDPOINTS.newGame}
            >
              <NewGame isAuthorized={isUserLoggedIn} handleLogout={setUserLoggedIn}/>
            </Route>
            <Route
              path={ROUTER_ENDPOINTS.game}
            >
              <Game isAuthorized={isUserLoggedIn} handleLogout={setUserLoggedIn}/>
            </Route>
            <UnregisteredRoute
              exact
              path={ROUTER_ENDPOINTS.greetings}
              component={GreetingsPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.signIn}
              component={SignInPage}
              isAuthorized={isUserLoggedIn}
              setUserLogged={setUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.signUp}
              component={SignUpPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.emailVerification}
              component={VerifyEmailPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.restoreMail}
              component={RestorePwdMailPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.restorePwd}
              component={RestorePwdPage}
              isAuthorized={isUserLoggedIn}
            />
            <UnregisteredRoute
              path={ROUTER_ENDPOINTS.newPassword}
              isAuthorized={isUserLoggedIn}
            />
            <PrivateRoute
              to={ROUTER_ENDPOINTS.home}
              component={HomePage}
              isAuthorized={isUserLoggedIn}
              setUserLoggedIn={setUserLoggedIn}
            />
            <Route
              path="*"
              component={NotFound}
            />
          </Switch>
        </BrowserRouter>
      )}
    </div>
  );
}

const PrivateRoute = ({
  component: Component,
  isAuthorized: isAuthorized,
  setUserLoggedIn: setUserLoggedIn,
  ...rest
}) => (
  <Route
    {...rest}
    render={(props) => {
      // eslint-disable-next-line no-unused-expressions
      return isAuthorized ? (
        <Component {...props} handleLogout={setUserLoggedIn} isAuthorized={isAuthorized}/>
      ) : (
        <Redirect to="/" />
      );
    }}
  />
);

const UnregisteredRoute = ({
  component: Component,
  isAuthorized: isAuthorized,

  ...rest
}) => (
  <Route
    {...rest}
    render={(props) => {
      // eslint-disable-next-line no-unused-expressions
      return !isAuthorized ? (
        <Component {...props} {...rest} />
      ) : (
        <Redirect to="/home" />
      );
    }}
  />
);

export default App;
