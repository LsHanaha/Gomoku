import React from 'react';

import { Button } from 'semantic-ui-react'

import {GoStone} from "components/goStone/goStone";
import styles from './humanBar.module.css'


export const HumanBar = (props) => {

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
      <div className={styles.buttonContainer}>
        <Button secondary size="massive" onClick={() => props.help()}>Help</Button>
      </div>
    </div>
  )
}
