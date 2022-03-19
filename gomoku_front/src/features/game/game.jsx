import React from 'react';
import { useState, useEffect } from "react";
import {TransitionablePortal, Segment} from "semantic-ui-react";

import {Navbar} from "components/navbar/navbar";
import { GreetingsFooter } from "components/greetingsFooter";
import { HumanBar } from 'components/gamers/human/humanBar';
import { RobotBar } from 'components/gamers/robot/robotBar';
import {postQueries} from "services/game/gameQueries";
import {GAME_ENDPOINTS, GAME_LOCAL_STORAGE} from "services/constants";

import styles from "./game.module.css";


export const Game = (props) => {

  const [startGameData, setStartGameData] = useState({});
  const [score, setScore] = useState([0, 0]);
  const [duration, setDuration] = useState(0);
  const [currentPlayer, setCurrentPlayer] = useState(1);
  const [currentTurn, setCurrentTurn] = useState(1);

  const [portalText, setPortalText] = useState("");
  const [portalOpen, setPortalOpen] = useState(false);

  const closePortal = () => {
    setPortalText("");
    setPortalOpen(false);
  }
  useEffect(() => {
    const id = setTimeout(() => {
      setPortalText("");
      setPortalOpen(false);
    }, 5000);
    return () => {
      clearTimeout(id);
    };
  }, [portalText]);

  useEffect(() => {
    const query = async () => {
      try {
        // debugger;
        const result = await postQueries(GAME_ENDPOINTS.gameStart,
          {uuid: localStorage.getItem(GAME_LOCAL_STORAGE.uuid)});
        setStartGameData(result.data);
        setScore(result.data.score);
        setCurrentPlayer(result.data.current_player);
        setCurrentTurn(result.data.count_of_turns)
        console.log(result.data);
      } catch (error){
        setPortalOpen(true);
        setPortalText(JSON.parse(error.message).detail || error.message);
      }
    };
    query();
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.container__inner}>
        <Navbar handleLogout={props.handleLogout} isAuthorized={props.isAuthorized}/>
        <div className={styles.game_container}>

          <div className={styles.game}>
            <div className={styles.user1}>
              <div className={styles.user}  style={currentPlayer === 1 ? {backgroundColor: '#2998ff'} : {}}>
                <HumanBar userId={1} score={score[0]} dice={startGameData.dices ? startGameData.dices[0] : 0}/>
              </div>
            </div>
            <div className={styles.board}>
              <div className={styles.boardData}>
                rule "{startGameData.rule}"
                <span className={styles.turn}>turn - {currentTurn}</span>
              </div>
              <div>board</div>
            </div>
            <div className={styles.user2}>
              <div className={[styles.user]}  style={currentPlayer === 2 ? {backgroundColor: '#2998ff'} : {}}>
                {startGameData.game_mode === 'hotseat' &&
                  <HumanBar userId={2} score={score[1]} dice={startGameData.dices ? startGameData.dices[1] : 0}/>}
                {startGameData.game_mode === 'robot' &&
                  <RobotBar userId={"robot"} score={score[1]} dice={startGameData.dices ? startGameData.dices[1] : 0}
                    duration={duration} debug={startGameData.debug}
                  />}
              </div>
            </div>
          </div>

          <TransitionablePortal
            closeOnTriggerClick
            onClose={closePortal}
            open={portalOpen}
          >
            <Segment
              style={{ left: 'calc(50% - 20rem)', position: 'fixed', top: 'calc(50% - 5rem)',
                zIndex: 1000, width: '40rem', height: '10rem', backgroundColor: 'pink' }}
            >
              <div className={styles.popup}>
                {portalText}
              </div>
            </Segment>
          </TransitionablePortal>

          <div className={styles.footer}>
            <GreetingsFooter />
          </div>
        </div>
      </div>
    </div>
  )
}
