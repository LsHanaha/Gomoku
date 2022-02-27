// /* eslint-disable react/jsx-props-no-spreading */
// /* eslint-disable no-else-return */
// /* eslint-disable import/prefer-default-export */
// /* eslint-disable react/prop-types */
// /* eslint-disable-next-line import/named */
import React, { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import { useForm } from "react-hook-form";

import { GreetingsFooter } from "components/greetingsFooter";
import { GreetingsContainer } from "components/greetingsContainer/GreetingsContainer";

import { postQueries } from "services/apiQueries";
import { storeTokens } from "services/auth/storeTokens";
import { ROUTER_ENDPOINTS, BACKEND_ENDPOINTS } from "services/constants";
import styles from "./SignInPage.module.css";

export const SignInPage = (props) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [errorMessage, setErrorMessage] = useState("");
  const history = useHistory();
  const onSubmit = async (data) => {
    try {
      const response = await postQueries(
        `${BACKEND_ENDPOINTS.auth}${BACKEND_ENDPOINTS.signIn}`,
        data
      );

      props.setUserLogged(true);
      storeTokens(response.data);

      history.push(ROUTER_ENDPOINTS.home);
    } catch (error) {
      setErrorMessage(JSON.parse(error.message).detail);
      const id = setTimeout(() => {
        setErrorMessage("");
      }, 5000);
      return () => {
        clearTimeout(id);
      };
    }
  };

  const checkUser = (data) => {
    const emailIsFromSchool = "^[A-Za-z0-9._%+-].*.$";
    const notEmail = "^[A-Za-z0-9._-]+$";

    return Boolean(data.match(emailIsFromSchool) || data.match(notEmail));
  };

  const emailError = () => {
    if (errors.username && !errors.username.message) {
      return "Wrong Username of Password";
    }
    return errors.username?.message || "";
  };

  return (
    <GreetingsContainer>
      <div className={styles.page_container}>
        <div className={styles.page_container_header}>
          <Link to={ROUTER_ENDPOINTS.greetings} className={styles.page_label}>
            Gomoku
          </Link>
        </div>
        <div className={styles.page_container_about}>sign in</div>

        <div className={styles.form}>
          <form
            onSubmit={handleSubmit(onSubmit)}
            className={styles.form__container}
          >
            <div className={styles.form_field__container}>
              <label className={styles.form__label}>
                Username or Email
                <input
                  type="text"
                  placeholder="email@email.com"
                  name="username"
                  className={styles.form__text}
                  {...register("username", {
                    validate: checkUser,
                    minLength: {
                      value: 4,
                      message: "Username too short, at least 4 symbols",
                    },
                    required: "Username or Email required",
                  })}
                />
              </label>

              <p className={styles.form__field_error}>{emailError()}</p>
            </div>
            <div className={styles.form_field__container}>
              <label className={styles.form__label}>
                Password
                <input
                  type="password"
                  name="password"
                  className={styles.form__pwd}
                  {...register("password", {
                    required: "Password Required",
                    minLength: {
                      value: 6,
                      message: "Password Too short, at least 6 symbols",
                    },
                  })}
                />
              </label>

              <p className={styles.form__field_error}>
                {!errors.username && errors.password
                  ? errors.password.message
                  : ""}
              </p>
            </div>
            <input type="submit" className={styles.form__submit} />
          </form>
        </div>

        <div className={styles.form__back_error}>
          {errorMessage ? `${errorMessage}` : ""}
        </div>

        <div className={styles.restore_pwd}>
          <Link
            className={styles.restore_pwd__link}
            to={ROUTER_ENDPOINTS.restoreMail}
          >
            Забыли пароль?
          </Link>
        </div>

        <GreetingsFooter />
      </div>
    </GreetingsContainer>
  );
};
