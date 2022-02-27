// /* eslint-disable react/jsx-props-no-spreading */
// /* eslint-disable-next-line import/prefer-default-export */

import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";

import { GreetingsFooter } from "components/greetingsFooter";
import { GreetingsContainer } from "components/greetingsContainer/GreetingsContainer";

import { postQueries } from "services/apiQueries";
import { ROUTER_ENDPOINTS, BACKEND_ENDPOINTS } from "services/constants";
import styles from "./RestorePasswordMailPage.module.css";

export function RestorePwdMailPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [errorMessage, setErrorMessage] = useState("");
  const [hasQueryResult, setQueryResult] = useState(false);

  useEffect(() => {
    const id = setTimeout(() => {
      setErrorMessage("");
    }, 5000);
    return () => {
      clearTimeout(id);
    };
  }, [errorMessage]);

  const onSubmit = async (data) => {
    try {
      const response = await postQueries(
        `${BACKEND_ENDPOINTS.auth}${BACKEND_ENDPOINTS.restorePassword}`,
        data
      );

      if (response.status === 201) {
        setQueryResult(true);
      }
    } catch (error) {
      setErrorMessage(JSON.parse(error.message).detail);
    }
  };

  const emailError = () => {
    if (errors.email && !errors.email.message) {
      return "Wrong Email. Only allowed 21 school emails";
    }

    return errors.email?.message || "";
  };

  return (
    <GreetingsContainer>
      <div className={styles.page_container}>
        <div className={styles.page_container_header}>
          <Link to={ROUTER_ENDPOINTS.greetings} className={styles.page_label}>
            Gomoku
          </Link>
        </div>

        <div className={styles.page_container_about}>Restore Password</div>

        {!hasQueryResult ? (
          <div className={styles.form}>
            <form
              onSubmit={handleSubmit(onSubmit)}
              className={styles.form__container}
            >
              <div className={styles.form_field__container}>
                <label className={styles.form__label}>
                  Введите почту, указанную Вами при регистрации.
                  <br />
                  На данный адрес будут высланы инструкции для восстановления
                  пароля.
                  <input
                    type="text"
                    placeholder="email@email.com"
                    name="email"
                    className={styles.form__text}
                    {...register("email", {
                      required: "Email required",
                    })}
                  />
                </label>

                <p className={styles.form__field_error}>{emailError()}</p>
              </div>
              <input type="submit" className={styles.form__submit} />
            </form>

            <div className={styles.form__back_error}>
              {errorMessage ? `Ошибка: ${errorMessage}` : ""}
            </div>
          </div>
        ) : (
          <div className={styles.form}>
            Письмо выслано. Проверьте почту, следуйте полученным инструкциям
          </div>
        )}
        <GreetingsFooter />
      </div>
    </GreetingsContainer>
  );
}
