// /* eslint-disable import/prefer-default-export */

import { Link } from "react-router-dom";

import { GreetingsFooter } from "components/greetingsFooter";
import { GreetingsContainer } from "components/greetingsContainer/GreetingsContainer";

import { ROUTER_ENDPOINTS } from "services/constants";
import styles from "./GreetingPage.module.css";
import React from "react";

export function GreetingsPage() {
  return (
    <GreetingsContainer>
      <div className={styles.greetings}>
        <div className={styles.greetings__header}>
          <h1 className={styles.header}>
            <span className={styles.header_main}>gomoku</span>
          </h1>
          <span className={styles.header_sub}>Some Japanese game</span>
        </div>

        <div className={styles.greetings__buttons}>
          <Link
            to={ROUTER_ENDPOINTS.signIn}
            className={styles.greetings__up_button}
          >
            <button
              type="button"
              className="btn btn--white btn--animated width-30-rem"
            >
              sign in
            </button>
          </Link>
          <Link
            to={ROUTER_ENDPOINTS.signUp}
            className={styles.greetings__low_button}
          >
            <button
              type="button"
              className="btn btn--white btn--animated width-30-rem"
            >
              sign up
            </button>
          </Link>
          <Link
            to={ROUTER_ENDPOINTS.newGame}
            className={styles.greetings__low_button}
          >
            <button
              type="button"
              className="btn btn--white width-30-rem btn--animated"
            >
              play without registration
            </button>
          </Link>
        </div>
        <GreetingsFooter />
      </div>
    </GreetingsContainer>
  );
}
