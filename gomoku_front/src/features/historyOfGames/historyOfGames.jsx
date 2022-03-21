import React from "react";
import {useState, useEffect} from "react";

import {Navbar} from "components/navbar/navbar";
import {GreetingsFooter} from "components/greetingsFooter";

import styles from './historyOfGames.module.css';
import {getQueries} from "../../services/game/gameQueries";
import {GAME_ENDPOINTS} from "../../services/constants";

export const HistoryOfGames = (props) => {

  const [userGames, setUserGames] = useState([]);

  useEffect(() => {
    const query = async () => {
      try {
        // debugger;
        const result = await getQueries(GAME_ENDPOINTS.history);
        setUserGames(result);
      } catch (error){
        console.log(error)
      }
    };
    query();
  }, []);

  const renderHistory = () => {
    if (!userGames)
      return <div></div>
    const res = userGames.map((game, i) => {
      return (
        <div key={`game-${i}`} className={styles.game}>
          <div className={styles.gameId}>{i + 1})</div>
          <div className={styles.gameMode}>{game.is_hot_seat ? "HotSeat" : "Robot"}</div>
          <div className={styles.winner}>{game.winner}</div>
          <div className={styles.result}>{game.result}</div>
          <div className={styles.moveCount}>{game.move_count}</div>
        </div>
      )
    });
    return res;
  }

  // [{"winner":"Player 2","move_count":27,"result":"{0,0}","is_hot_seat":true},{"winner":"Player 1","move_count":9,"result":"{0,0}","is_hot_seat":true},{"winner":"Player 1","move_count":9,"result":"{0,0}","is_hot_seat":true},{"winner":"Player 1","move_count":9,"result":"{0,0}","is_hot_seat":true},{"winner":"Player 1","move_count":9,"result":"{0,0}","is_hot_seat":true}]
  return (
    <div className={styles.container}>
      <div className={styles.container__inner}>
        <Navbar handleLogout={props.handleLogout} isAuthorized={props.isAuthorized}/>
        <div className={styles.history_container}>

          <div className={styles.main}>
            <div className={styles.header}>Game History</div>
            {!userGames &&
              <div className={styles.emptyHistory}>
                You still not finished any game!
              </div>
            }
            {userGames &&
              <>
                {renderHistory()}
              </>
            }

          </div>
          <div className={styles.footer}>
            <GreetingsFooter />
          </div>
        </div>
      </div>
    </div>
  )
}
