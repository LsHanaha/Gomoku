import React from 'react'
import { Dropdown } from 'semantic-ui-react'

import styles from './dropdownComponent.module.css';

export const DropdownExampleSelection = (props) => {
  let data = props.data;
  if (!data)
    return <div></div>;
  data = data.map((brick) => {
    return {key: brick.id, id: brick.id, text: brick.name, value: brick.id}
  })
  return (
    <Dropdown
      placeholder='Select Option'
      fluid
      selection
      options={data}
      value={props.selected}
      className={styles.fontSize}
      onChange={(e, {value}) => {props.setter(value)}}
    />
  )
}

export default DropdownExampleSelection
