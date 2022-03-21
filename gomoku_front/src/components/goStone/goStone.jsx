import React from 'react';


import styles from './goStone.module.css';


export const GoStone = (props) => {

  let color;
  switch (props.color) {
    case 'black':
      color = styles.black;
      break;

    case 'white':
      color = styles.white;
      break;

    case 'purple':
      color = styles.purple;
      break;

    case 'yellow':
      color = styles.yellow
      break;

    case 'blue':
      color = styles.blue
      break;

    case 'red':
      color = styles.red;
      break;
  }

  let stoneStyle = `${styles.stone} ${color}`

  if (props.large) {
    stoneStyle = `${stoneStyle} ${styles.large}`
  }

  return (
    <div className={stoneStyle}>
    </div>
  )

}
