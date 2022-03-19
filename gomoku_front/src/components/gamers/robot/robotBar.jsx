import React from 'react';
import {GoStone} from "../../goStone/goStone";

import styles from './robotBar.module.css';


export const RobotBar = (props) => {
  return (
    <div className={styles.container}>
      <div className={styles.user}>user {props.userId}</div>
      <div className={styles.dice}>
        dice
        <div className={styles.goStone}>
          <GoStone large={true} color={props.dice}/>
        </div>
      </div>
      <div className={styles.score}>
        score
        <div className={styles.scoreValue}>
          {props.score}
        </div>
      </div>
      <div className={styles.duration}>
        turn duration
        <div className={styles.durationValue}>
          {props.duration} ms
        </div>
      </div>
      <div className={styles.debugStatus}>
        {props.debug ? "debug mode activated" : ""}
      </div>
    </div>
  )
}
