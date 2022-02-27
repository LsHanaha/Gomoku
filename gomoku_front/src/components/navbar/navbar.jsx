import React from 'react';
import { Link, useHistory } from "react-router-dom";

import {deleteTokens} from "services/auth/storeTokens";
import {ROUTER_ENDPOINTS, GAME_LOCAL_STORAGE} from "services/constants";

import styles from "./navbar.module.css";


const performLogout = async (setUserLoggedIn) => {

    await setUserLoggedIn(false);
    await deleteTokens();
}


export const Navbar = (props) => {

  const homePageLink = localStorage.getItem(GAME_LOCAL_STORAGE.uuid)
    ? ROUTER_ENDPOINTS.game
    : ROUTER_ENDPOINTS.newGame;

  return (
    <div className={styles.main}>
      <Link
          to={homePageLink}
          className={styles.homeLink}
      >
          Gomoku
      </Link>
      <Link
          to={ROUTER_ENDPOINTS.newGame}
          className={styles.otherLink}
      >
          new game
      </Link>
      <Link
          to={ROUTER_ENDPOINTS.history}
          className={styles.otherLink}
      >
          history
      </Link>

      {props.isAuthorized &&
        <Link to={ROUTER_ENDPOINTS.greetings} className={styles.logout} onClick={() => performLogout(props.handleLogout)}>
            logout
        </Link>

      }
      {!props.isAuthorized &&
        <div className={styles.signGroup}>
          <Link to={ROUTER_ENDPOINTS.signIn}>
            <div className={styles.signIn}>
              sign in
            </div>
          </Link>
          <span className={styles.signDelimiter}>|</span>
          <Link to={ROUTER_ENDPOINTS.signUp}>
            <div className={styles.signUp}>
              sign up
            </div>
          </Link>
        </div>
      }
    </div>
  )
}
