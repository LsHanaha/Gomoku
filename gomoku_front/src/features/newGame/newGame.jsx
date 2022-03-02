import React from 'react';
import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import {ToggleButton, ToggleButtonGroup} from "react-bootstrap";
import {Icon} from 'semantic-ui-react'

import { getQueries, postQueries } from "services/game/gameQueries";
import { ROUTER_ENDPOINTS, GAME_ENDPOINTS, GAME_LOCAL_STORAGE } from "services/constants";

import { GreetingsFooter } from "components/greetingsFooter";
import {Navbar} from "components/navbar/navbar";
import {DropdownExampleSelection} from 'components/dropdown/dropdownComponent';
import {Popup} from 'components/popup/Popup';
import {RadioButtons} from "components/radioButtons/radioButtons";
import {SmallField} from "components/smallField/smallField";
import {SelectDices} from "components/selectDices/selectDices";

import styles from "./newGame.module.css";


export const NewGame = (props) => {

  const [isHotSeat, setHotSeat] = useState(false);
  const [complexities, setComplexities] = useState(null);
  const [algorithms, setAlgorithms] = useState(null);
  const [rules, setRules] = useState(null);

  const [complexity, setComplexity] = useState(1);
  const [algorithm, setAlgorithm] = useState(1);
  const [rule, setRule] = useState(1);

  const [isDebug, setDebug] = useState(false);
  const [field, setField] = useState('default');
  const [fieldPopup, setFieldPopup] = useState(false);
  const [diceColors, setDiceColors] = useState(["black", "white"]);
  const [startGameLoader, setStartGameLoader] = useState(false);

  const [errorMessage, setErrorMessage] = useState(null);

  const dicesColorsOptions = ["black", 'white', 'blue', 'yellow', 'red'];
  const history = useHistory();

  const handleSubmit = async () => {
    await setStartGameLoader(true);
    try {
      const res = await postQueries(GAME_ENDPOINTS.newGame, {
        'field': field,
        'dices': diceColors,
        'hot_seat': isHotSeat,
        'difficulty': complexity,
        'algorithm': algorithm,
        'rule': rule,
        'is_debug': isDebug
      })
      if (res.data && res.data.uuid) {
        localStorage.removeItem(GAME_LOCAL_STORAGE.uuid);
        localStorage.setItem(GAME_LOCAL_STORAGE.uuid, res?.data?.uuid);
        const new_game = await postQueries(GAME_ENDPOINTS.startGame, {uuid: res.data.uuid})
        if (new_game?.data?.status)
          history.push(ROUTER_ENDPOINTS.game);
        else
          throw new Error("Error while starting new game");
      }
    } catch (error) {
      setStartGameLoader(false);
      setErrorMessage(JSON.parse(error.message).detail);
    }
  }

  useEffect(() => {
    const query = async () => {
      try {
        const data = await getQueries(GAME_ENDPOINTS.newGame);
        await setComplexities(data.difficulties);
        await setAlgorithms(data.algorithms);
        await setRules(data.rules);
      } catch (error) {
        setErrorMessage(JSON.parse(error.message).detail);
      }
    }
    query();
  }, [])

  useEffect(() => {
    const id = setTimeout(() => {
      setErrorMessage("");
    }, 5000);
    return () => {
      clearTimeout(id);
    };
  }, [errorMessage]);

  return (
    <div className={styles.container}>
      <div className={styles.container__inner}>
        <Navbar handleLogout={props.handleLogout} isAuthorized={props.isAuthorized}/>
        <div className={styles.start_container}>

          <div className={styles.page_header}>
            Select game parameters
          </div>

          <div className={styles.hotSeatContainer}>

            <div className={styles.description}>
              select opponent
            </div>
            <ToggleButtonGroup name="radio" type="radio" defaultValue={[false]} value={isHotSeat}
                               className={styles.hotSeatButtons}>
              <ToggleButton
                className={[styles.hotSeatButton, styles.hotSeatButtonLeft, isHotSeat ? styles.activateHotSeat : ""]}
                key="1"
                id="radio-1"
                type="radio"
                variant="secondary"
                name="radio"
                value={true}
                checked={isHotSeat}
                onChange ={() => setHotSeat(true)}
              >
                Human
              </ToggleButton>
              <ToggleButton
                className={[styles.hotSeatButton, styles.hotSeatButtonRight, !isHotSeat ? styles.activateHotSeat : ""]}
                key="2"
                id="radio-2"
                type="radio"
                variant="secondary"
                name="radio"
                value={false}
                checked={!isHotSeat}
                onChange={() => setHotSeat(false)}
              >
                AI
              </ToggleButton>
            </ToggleButtonGroup>
          </div>

          <div className={styles.anotherFieldsContainer}>

            <div className={styles.error_message}>
              {errorMessage ? `Ошибка: ${errorMessage}` : null}
            </div>
            {isHotSeat &&
                <div className={styles.dicesContainer}>
                  <div className={styles.diceText}>
                    dice colors
                  </div>
                  <SelectDices diceColors={diceColors} dicesColorsOptions={dicesColorsOptions}
                               setter={setDiceColors}/>
                </div>
            }
            {!isHotSeat &&
              <>
                <div className={styles.aiContainer}>
                  <div className={styles.complexityContainer}>
                    <div className={styles.description}>
                    complexity
                    </div>
                    <DropdownExampleSelection data={complexities} setter={setComplexity} selected={complexity}/>
                  </div>
                  <div className={styles.algorithmContainer}>
                    <div className={styles.description}>
                      algorithm
                    </div>
                    <DropdownExampleSelection data={algorithms} setter={setAlgorithm} selected={algorithm}/>
                  </div>
                </div>
                <div className={styles.debugContainer}>

                  <div className="ui segment">
                    <div className="ui toggle checkbox">

                      <input value={isDebug}  onChange={() => setDebug(!isDebug)} type="checkbox"/>
                      <label className={styles.debugLabel}>Debug Mode</label>

                    </div>
                  </div>
                </div>
              </>
            }
            <div className={styles.rulesContainer}>
              <div className={styles.ruleText}>
                Select Rule
              </div>
              <div className={styles.rulesButtons}>
                <RadioButtons data={rules} value={rule} setter={setRule} groupName="rules"/>
              </div>
            </div>
            <div className={styles.fieldContainer}>
              <button
                type="button"
                className="btn btn--gray width-30-rem"
                onClick={() => setFieldPopup(!fieldPopup)}
              >
                select field
              </button>
            </div>
          </div>

          {fieldPopup &&
            <Popup hidePopup={setFieldPopup}>
              <div className={styles.fieldContent}>
                <div className={styles.fieldContentHeader}>
                  Select Field
                </div>

                <div className={styles.fieldContentFields}>
                  <div className={[field === 'default' ? styles.fieldSelected : styles.fieldContentFieldContainer]}
                       onClick={() => setField('default')}>
                    <div className={styles.fieldContentField}>
                      <SmallField first="black" second="white"/>
                    </div>
                    <div className={styles.fieldContentFieldName}>
                      Black And White
                    </div>
                  </div>

                  <div className={[field === 'color' ? styles.fieldSelected : styles.fieldContentFieldContainer]}
                       onClick={() => setField('color')}>
                    <div className={styles.fieldContentField}>
                      <SmallField first="blue" second="yellow"/>
                    </div>
                    <div className={styles.fieldContentFieldName}>
                      blue and yellow
                    </div>
                  </div>

                  <div className={[field === 'wood' ? styles.fieldSelected : styles.fieldContentFieldContainer]}
                       onClick={() => setField('wood')}>
                    <div className={styles.fieldContentField}>
                      <SmallField first="" second="" background={true}/>
                    </div>
                    <div className={styles.fieldContentFieldName}>
                      wood
                    </div>
                  </div>

                </div>
                <div className={styles.fieldContentButton}>
                  <button
                    type="button"
                    className="btn btn--gray width-30-rem"
                    onClick={() => setFieldPopup(!fieldPopup)}
                  >
                    Close
                  </button>
                </div>
              </div>
            </Popup>
          }

          <button
            type="button"
            className="btn btn--white width-30-rem"
            onClick={() => handleSubmit()}
          >
            start game
          </button>

          <div className={styles.footer}>
            <GreetingsFooter />
          </div>

          {startGameLoader &&
            <div className="popup popup--visible">
              <div className={styles.loaderContainer}>
                <Icon loading size='massive' name='circle notch' />
                Preparing field
              </div>
            </div>
          }
        </div>
      </div>
    </div>
  )
}

