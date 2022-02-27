import React from 'react';
import { useState, useEffect } from "react";

import {Navbar} from "components/navbar/navbar";
import { GreetingsFooter } from "components/greetingsFooter";
import styles from "./game.module.css";

export const Game = (props) => {

  return (
    <div className={styles.container}>
      <div className={styles.container__inner}>
        <Navbar handleLogout={props.handleLogout} isAuthorized={props.isAuthorized}/>
        <div className={styles.game_container}>

          <div className={styles.game}>
            <div className={styles.user1}>
              <div className={styles.user}>
                user1
              </div>
            </div>
            <div className={styles.board}>
              board
            </div>
            <div className={styles.user2}>
              <div className={[styles.user]}>
                user2
              </div>
            </div>
          </div>
          <div className={styles.footer}>
            <GreetingsFooter />
          </div>
        </div>
      </div>
    </div>
  )
}
