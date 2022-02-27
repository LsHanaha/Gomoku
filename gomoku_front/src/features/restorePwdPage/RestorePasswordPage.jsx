// /* eslint-disable react/jsx-props-no-spreading */
// /* eslint-disable no-return-assign */
// /* eslint-disable import/prefer-default-export */
import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { useForm } from "react-hook-form";

import { GreetingsFooter } from "components/greetingsFooter";
import { GreetingsContainer } from "components/greetingsContainer/GreetingsContainer";

import { getQueries, postQueries } from "services/apiQueries";
import { ROUTER_ENDPOINTS, BACKEND_ENDPOINTS } from "services/constants";
import styles from "./RestorePasswordPage.module.css";

export function RestorePwdPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    getValues,
  } = useForm();

  const [restoreMailToken, setRestoreMailToken] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [restoreToken, setRestoreToken] = useState("");
  const [hasPwdUpdated, setPwdUpdated] = useState(false);
  const [restoreMessage, setRestoreMessage] = useState("");
  const { search } = useLocation();

  useEffect(async () => {
    const params = new URLSearchParams(search);
    const tokenFromMailRestore = params.get("token");
    try {
      if (!tokenFromMailRestore) {
        setErrorMessage("Token for restore password not found");
      }
      const response = await getQueries(
        `${BACKEND_ENDPOINTS.auth}${BACKEND_ENDPOINTS.restorePassword}`,
        {
          token: tokenFromMailRestore,
        }
      );

      if (response.status === 200 && !restoreToken) {
        setRestoreToken(response.data["restore-token"]);
        setRestoreMessage(response.data.message);
        setRestoreMailToken(tokenFromMailRestore);
      }
    } catch (error) {
      setRestoreMessage(JSON.parse(error.message).detail);
    }
  }, [restoreToken, search]);

  const onSubmit = async (data) => {
    try {
      const response = await postQueries(
        `${BACKEND_ENDPOINTS.auth}${BACKEND_ENDPOINTS.newPassword}`,
        {
          ...data,
          ...{ token: restoreToken, restore_mail_token: restoreMailToken },
        }
      );
      if (response.status === 201) {
        setRestoreMessage(response.data.message);
        setPwdUpdated(true);
      }
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

  return (
    <GreetingsContainer>
      <div className={styles.page_container}>
        <div className={styles.page_container_header}>
          <Link to={ROUTER_ENDPOINTS.greetings} className={styles.page_label}>
            Gomoku
          </Link>
        </div>
        <div className={styles.page_container_about}>Restore Password</div>

        {!restoreToken ? (
          <div className={styles.form_field__container}>
            {restoreMessage ||
              "Проводится проверка прав на восстановление пароля"}
          </div>
        ) : (
          <div className={styles.form}>
            {!hasPwdUpdated ? (
              <form
                onSubmit={handleSubmit(onSubmit)}
                className={styles.form__container}
              >
                <div className={styles.form_field__container}>
                  {restoreMessage}
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

                  <label className={styles.form__label}>
                    Confirm Password
                    <input
                      type="password"
                      name="confirmPassword"
                      className={styles.form__pwd}
                      {...register("confirmPassword", {
                        validate: {
                          matchesPreviousPassword: (value) => {
                            const { password } = getValues();
                            return (
                              password === value || "Passwords should match!"
                            );
                          },
                        },
                      })}
                    />
                  </label>

                  <p className={styles.form__field_error}>
                    {errors.password?.message ||
                      errors.confirmPassword?.message ||
                      ""}
                  </p>
                </div>
                <input type="submit" className={styles.form__submit} />
              </form>
            ) : (
              <div>
                <div>
                  Пароль успешно обновлен! Теперь вы можете зайти в приложение
                </div>
              </div>
            )}

            <div className={styles.form__back_error}>
              {errorMessage ? `Ошибка: ${errorMessage}` : ""}
            </div>
          </div>
        )}
        <GreetingsFooter />
      </div>
    </GreetingsContainer>
  );
}
