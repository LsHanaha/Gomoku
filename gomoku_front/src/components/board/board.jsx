import React from "react";

import { GoStone } from "../goStone/goStone";

import styles from './board.module.css';


export const Board = (props) => {
  console.log("board");
  const createRow = (row, rowId) => {

    const res = row.map((cell, colId) => {
      return (
        <div key={`cell-${rowId}-${colId}`} className={styles.cell}>
          {cell ?
            <GoStone color={cell === 3 ? 'purple' : props.dices[cell - 1]}/>
            :
            <div className={styles.emptyCell} onClick={() => props.placeStone(rowId, colId)} />
          }
        </div>
      )
    });

    return res;
  }

  const createField = (field) => {
    const res = field.map((row, rowId) => {
      return (
        <div key={`row-${rowId}`} className={styles.boardRow}>
          {createRow(row, rowId)}
        </div>
      )
    })
    return res;
  }

  return (
    <div className={styles.board}>
      <div className={props.fieldName === 'default' ? styles.boardDefault : styles.boardWood}>
        {createField(props.field)}
      </div>
    </div>
  )
}
