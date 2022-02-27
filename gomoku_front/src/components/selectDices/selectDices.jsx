import React from "react";

import {GoStone} from "components/goStone/goStone";
import {Icon} from 'semantic-ui-react';

import styles from "./selectDices.module.css";


const buttonUp = (props, userId) => {

  let diceOfUser1 = props.dicesColorsOptions.indexOf(props.diceColors[0]);
  let diceOfUser2 = props.dicesColorsOptions.indexOf(props.diceColors[1]);
  const size = props.dicesColorsOptions.length;
  let userColorId;

  if (userId === 0) {
    if ((diceOfUser1 + 1) % size === diceOfUser2)
      diceOfUser1 = diceOfUser1 + 1;
    userColorId = (diceOfUser1 + 1) % size;
  } else {
    if ((diceOfUser2 + 1) % size === diceOfUser1)
      diceOfUser2 = diceOfUser2 + 1;
    userColorId = (diceOfUser2 + 1) % size;
  }

  const temp = [...props.diceColors];
  temp[userId] = props.dicesColorsOptions[userColorId];
  props.setter(temp);
}

const buttonDown = (props, userId) => {
  let diceOfUser1 = props.dicesColorsOptions.indexOf(props.diceColors[0]);
  let diceOfUser2 = props.dicesColorsOptions.indexOf(props.diceColors[1]);
  const size = props.dicesColorsOptions.length;
  let userColorId;

  if (userId === 0) {
    if (diceOfUser1 - 1 < 0)
      diceOfUser1 = size;
    if ((diceOfUser1 - 1) === diceOfUser2)
      --diceOfUser1;
    if (diceOfUser1 - 1 < 0)
      diceOfUser1 = size;
    userColorId = diceOfUser1 - 1;
  } else {
    if (diceOfUser2 - 1 < 0)
      diceOfUser2 = size;
    if ((diceOfUser2 - 1) === diceOfUser1)
      --diceOfUser2;
    if (diceOfUser2 - 1 < 0)
      diceOfUser2 = size;
    userColorId = diceOfUser2 - 1;
  }

  const temp = [...props.diceColors];
  temp[userId] = props.dicesColorsOptions[userColorId];
  props.setter(temp);
}


export const SelectDices = (props) => {
  if (!props.diceColors)
    return <div></div>

  return (
    <div className={styles.dices}>
      <div className={styles.innerDiceContainer}>
        <div className={styles.diceText}>player 1</div>
        <div className={styles.diceUp} onClick={() => {
          buttonUp(props, 0);
        }}>
          <Icon name='angle up' size='huge'/>
        </div>
        <div className={styles.dice} >
          <GoStone large={true} color={props.diceColors[0]}/>
        </div>
        <div className={styles.diceDown} onClick={() => buttonDown(props, 0)}>
          <Icon name='angle down' size='huge'/>
        </div>

      </div>
      <div className={styles.innerDiceContainer}>
        <div className={styles.diceText}>player 2</div>

        <div className={styles.diceUp} onClick={() => {
          buttonUp(props, 1);
        }}>
          <Icon name='angle up' size='huge'/>
        </div>
        <div className={styles.dice}>
          <GoStone large={true} color={props.diceColors[1]}/>
        </div>
        <div className={styles.diceDown} onClick={() => buttonDown(props, 1)}>
          <Icon name='angle down' size='huge'/>
        </div>
      </div>
    </div>
  )
}