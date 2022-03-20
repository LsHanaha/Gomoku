import React from 'react';


import styles from './smallField.module.css';


export const SmallField = (props) => {

  const additional = props.background === "default" ? styles.backgroundDefaultField : styles.backgroundWoodField;

  return (
    <div className={additional}>
      <div className={styles.fieldRow}>
        <div className={styles.fieldCell} style={{'backgroundColor': props.first}}>

        </div>
        <div className={styles.fieldCell} style={{'backgroundColor': props.second}}>

        </div>
      </div>
      <div className={styles.fieldRow}>
        <div className={styles.fieldCell} style={{'backgroundColor': props.second}}>

        </div>
        <div className={styles.fieldCell} style={{'backgroundColor': props.first}}>

        </div>
      </div>
    </div>
  )
}
