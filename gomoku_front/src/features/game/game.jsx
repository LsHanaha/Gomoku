import React from 'react';
import { useState, useEffect } from "react";
import {useHistory} from "react-router-dom";
import {TransitionablePortal, Segment} from "semantic-ui-react";

import {Navbar} from "components/navbar/navbar";
import { GreetingsFooter } from "components/greetingsFooter";
import { HumanBar } from 'components/gamers/human/humanBar';
import { RobotBar } from 'components/gamers/robot/robotBar';
import { Board } from 'components/board/board';
import {postQueries} from "services/game/gameQueries";
import {GAME_ENDPOINTS, GAME_LOCAL_STORAGE} from "services/constants";

import styles from "./game.module.css";


export const Game = (props) => {

  const history = useHistory();

  const [gameEndData, setGameEndData] = useState(null);

  const [startGameData, setStartGameData] = useState({});
  const [score, setScore] = useState([0, 0]);
  const [duration, setDuration] = useState(0);
  const [currentPlayer, setCurrentPlayer] = useState(1);
  const [currentTurn, setCurrentTurn] = useState(1);
  const [field, setField] = useState([[]]);

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
        const result = await postQueries(GAME_ENDPOINTS.gameStart,
          {uuid: localStorage.getItem(GAME_LOCAL_STORAGE.uuid)});
        if (!result.data) {
          setPortalText("Game not exist. Start new one!");
          setPortalOpen(true);
          setTimeout(() => {
            history.push(GAME_ENDPOINTS.newGame);
          }, 5000);
        }
        setStartGameData(result.data);
        setScore(result.data.score);
        setCurrentPlayer(result.data.current_player);
        setCurrentTurn(result.data.count_of_turns)
        setField(result.data.field);
      } catch (error){
        setPortalOpen(true);
        setPortalText(JSON.parse(error.message).detail || error.message);
      }
    };
    query();
  }, []);

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  const placeDebug = async (debugData, rowId, colId) => {
    const startField = field;
    let tempVal;
    if (rowId && colId) {
      startField[rowId][colId] = 1;
      setField(startField);
    }

    for (let move of debugData) {
      let tempField = [...startField];
      tempVal = tempField[move[0]][move[1]];
      tempField[move[0]][move[1]] = 3;
      setField(tempField);
      await sleep(500);
      tempField[move[0]][move[1]] = tempVal;
    }
  }

  const continueGame = async (data, rowId, colId) => {
    if (data.debug)
      await placeDebug(data.debug, rowId, colId);
    await setCurrentPlayer(data.current_player);
    await setCurrentTurn(data.count_of_turns)
    await setDuration(data.robot_time || 0);
    await setScore(data.score);
    await setField(data.map);
  }

  const endGame = async (data) => {
    setGameEndData(data);
    localStorage.removeItem(GAME_LOCAL_STORAGE.uuid);
    setTimeout(() => {
      history.push(GAME_ENDPOINTS.newGame);
    }, 20000);
  }


  const placeStone = async (rowId, colId) => {
    try {
      const response = await postQueries(GAME_ENDPOINTS.move, {
        row: rowId,
        col: colId,
        uuid: localStorage.getItem(GAME_LOCAL_STORAGE.uuid)
      });
      if (response.data.game_continue)
        await continueGame(response.data.game_continue, rowId, colId)
      if (response.data.game_end)
        await endGame(response.data.game_end)

    } catch (error) {
      setPortalOpen(true);
      setPortalText(JSON.parse(error.message).detail || error.message);
    }
  }

  const callForHelp = async () => {
    try {
      const response = await postQueries(GAME_ENDPOINTS.help, {
        uuid: localStorage.getItem(GAME_LOCAL_STORAGE.uuid)
      });
      if (response.data.game_continue)
        await continueGame(response.data.game_continue)
      if (response.data.game_end)
        await endGame(response.data.game_end)

    } catch (error) {
      setPortalOpen(true);
      setPortalText(JSON.parse(error.message).detail || error.message);
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.container__inner}>
        <Navbar handleLogout={props.handleLogout} isAuthorized={props.isAuthorized}/>
        <div className={styles.game_container}>

          {!gameEndData &&
            <div className={styles.game}>
              <div className={styles.user1}>
                <div className={styles.user}  style={currentPlayer === 1 ? {backgroundColor: '#2998ff'} : {}}>
                  <HumanBar userId={1} score={score[0]} dice={startGameData.dices ? startGameData.dices[0] : 0}
                            help={callForHelp} currentPlayer={currentPlayer}
                  />
                </div>
              </div>
              <div className={styles.board}>
                <div className={styles.boardData}>
                  rule "{startGameData.rule}"
                  <span className={styles.turn}>turn - {currentTurn}</span>
                </div>
                <div className={styles.boardBoard}>
                  <Board fieldName={startGameData.field_name} field={field} dices={startGameData.dices}
                    currentPlayer={currentPlayer} placeStone={placeStone}
                  />
                </div>
              </div>
              <div className={styles.user2}>
                <div className={[styles.user]}  style={currentPlayer === 2 ? {backgroundColor: '#2998ff'} : {}}>
                  {startGameData.game_mode === 'hotseat' &&
                    <HumanBar userId={2} score={score[1]} dice={startGameData.dices ? startGameData.dices[1] : 0}
                              help={callForHelp} currentPlayer={currentPlayer}
                    />}
                  {startGameData.game_mode === 'robot' &&
                    <RobotBar userId={"robot"} score={score[1]} dice={startGameData.dices ? startGameData.dices[1] : 0}
                      duration={duration} debug={startGameData.debug}
                    />}
                </div>
              </div>
            </div>
          }
          {gameEndData &&
            <div className={styles.endGame}>
              <div className={styles.endHeader}>Congratulations!</div>
              <div className={styles.endWinner}>
                User {gameEndData.winner} won!
              </div>
              <div className={styles.endScore}>
                <div className={styles.endScoreHeader}>score</div>
                <div className={styles.endScoreValue}>{gameEndData.score[0]} - {gameEndData.score[1]}</div>
              </div>
              <div className={styles.endCountOfTurns}>
                <div className={styles.endTurnsHeader}>count of turns</div>
                <div className={styles.endTurnsValue}>{gameEndData.count_of_turns}</div>
              </div>
              <div className={styles.endMessage}>
                prepare for the new game!
              </div>
            </div>
          }
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
