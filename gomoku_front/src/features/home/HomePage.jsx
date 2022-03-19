// /* eslint-disable import/prefer-default-export */
import React from "react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {Navbar} from "components/navbar/navbar";

import { GreetingsFooter } from "components/greetingsFooter";
import {ROUTER_ENDPOINTS, GAME_ENDPOINTS, GAME_LOCAL_STORAGE} from "services/constants";
import { getQueries } from "services/game/gameQueries";

import styles from "./HomePage.module.css";


export function HomePage(props) {

  const [storedGameUUID, setStoredGameUUID] = useState(null);

  useEffect(() => {
    const query = async () => {
      try {
        const storedGame = await getQueries(GAME_ENDPOINTS.checkStored);
        setStoredGameUUID(storedGame?.uuid);
      } catch {
        setStoredGameUUID(false);
      }
    };
    query();
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.container__inner}>
        <Navbar handleLogout={props.handleLogout} isAuthorized={props.isAuthorized}/>
        <div className={styles.home_container}>
          <div className={styles.page_header}>
            Gomoku 42
          </div>
          <div className={styles.home_buttons_container}>
            <Link
              to={ROUTER_ENDPOINTS.newGame}
              className={styles.up_button}
            >
              <button
                type="button"
                className="btn btn--white width-30-rem"
              >
                new game
              </button>
            </Link>
            {storedGameUUID &&
              <Link
                to={ROUTER_ENDPOINTS.game}
                className={styles.up_button}
              >
                <button
                  type="button"
                  className="btn btn--white width-30-rem"
                  onClick={() => {localStorage.setItem(GAME_LOCAL_STORAGE.uuid, storedGameUUID)}}
                >
                  resume game
                </button>
              </Link>
            }
            <Link
              to={ROUTER_ENDPOINTS.history}
              className={styles.up_button}
            >
              <button
                type="button"
                className="btn btn--white width-30-rem"
              >
                history
              </button>
            </Link>
          </div>
          <div className={styles.footer}>
            <GreetingsFooter />
          </div>
        </div>
      </div>
    </div>
  );
}
