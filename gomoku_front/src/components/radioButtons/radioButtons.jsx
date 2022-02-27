import React from "react";


import styles from './radioButtons.module.css';
import {ToggleButton, ToggleButtonGroup} from "react-bootstrap";



export const RadioButtons = (props) => {

  if (!props.data)
    return <div></div>

  const toRender = props.data.map(row => {
    return (
      <ToggleButton
        className={[styles.button, row.id == props.value ? styles.buttonActive : ""]}
        key={`${props.groupName}-${row.id}`}
        id={`radio-${props.groupName}-${row.id}`}
        type="radio"
        variant="secondary"
        name="radio"
        value={row.id}
        checked={row.id == props.value}
        onChange ={(e, value) => props.setter(e.currentTarget.value)}
      >
        {row.name}
      </ToggleButton>
    )
  })
  return (
    <div>
      <ToggleButtonGroup name={props.groupName}
                         type="radio"
                         defaultValue={['1']}
                         // value={props.value}
                         className={styles.buttonsGroup}
      >
        {toRender}
      </ToggleButtonGroup>
    </div>
  )
}

