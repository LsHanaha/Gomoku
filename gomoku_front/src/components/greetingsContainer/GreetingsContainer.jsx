import styles from './GreetingsContainer.module.css';

export function GreetingsContainer(props) {
  return (
    <div className={styles.container}>
      <div className={styles.container__inner}>
        {props.children}
      </div>
    </div>
  );
}
