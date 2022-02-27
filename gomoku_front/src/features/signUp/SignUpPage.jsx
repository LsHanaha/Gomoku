// /* eslint-disable react/jsx-props-no-spreading */
// /* eslint-disable no-else-return */
// /* eslint-disable import/prefer-default-export */
// /* eslint-disable-next-line import/named */

import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";

import { GreetingsFooter } from "components/greetingsFooter";
import { GreetingsContainer } from "components/greetingsContainer/GreetingsContainer";

import { postQueries } from "services/apiQueries";
import { ROUTER_ENDPOINTS, BACKEND_ENDPOINTS } from "services/constants";
import styles from "./SignUpPage.module.css";

export function SignUpPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    getValues,
  } = useForm();

  const [errorMessage, setErrorMessage] = useState("");
  const [isRegistered, setRegistered] = useState(false);
  const SYMBOL = "\u00A0";

  const onSubmit = async (data) => {
    try {
      const response = await postQueries(
        `${BACKEND_ENDPOINTS.auth}${BACKEND_ENDPOINTS.signUp}`,
        data
      );
      if (response.status === 201) {
        setRegistered(true);
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

  const checkMail = (data) => {
    const emailIsFromSchool = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    const notEmail = "^[A-Za-z0-9._-]+$";
    if (data.match(emailIsFromSchool)) return true;
    return false;

  };

  const emailError = () => {
    let errorMsg = "";
    if (!errors.username && errors.email) {
      errorMsg = errors.email.message;
    } else if (errors.confirmEmail) {
      errorMsg = errors.confirmEmail.message;
    }
    return errorMsg;
  };

  const passwordError = () => {
    if (errors.email || errors.confirmEmail) {
      return "";
    }

    // if (!errors.email && errors.password) {
    //   errorMsg = errors.password.message;
    // } else if (
    //   !errors.email
    //   && !errors.confirmEmail
    //   && errors.confirmPassword
    // ) {
    //   errorMsg = errors.confirmPassword.message;
    // }

    return errors.password?.message || errors.confirmPassword?.message || "";
  };

  return (
    <GreetingsContainer>
      <div className={styles.page_container}>
        <div className={styles.page_container_header}>
          <Link to={ROUTER_ENDPOINTS.greetings} className={styles.page_label}>
            Gomoku
          </Link>
        </div>
        <div className={styles.page_container_about}>sign up</div>

        {!isRegistered ? (
          <div className={styles.form}>
            <form
              onSubmit={handleSubmit(onSubmit)}
              className={styles.form__container}
            >
              <div className={styles.form_field__container}>
                <label className={styles.form__label}>
                  Username
                  <input
                    type="text"
                    placeholder="username"
                    name="username"
                    className={styles.form__text}
                    {...register("username", {
                      minLength: {
                        value: 4,
                        message: "Username too short, at least 4 symbols",
                      },
                      required: "Username required",
                    })}
                  />
                </label>

                <p className={styles.form__field_error}>
                  {errors.username ? errors.username.message : SYMBOL}
                </p>
              </div>

              <div className={styles.form_field__container}>
                <div className={styles.form_field_width}>
                  <div className={styles.form_field_width_brick}>
                    <label className={styles.form__label}>
                      Email
                      <input
                        type="email"
                        placeholder="email@email.com"
                        name="email"
                        className={styles.form__text}
                        {...register("email", {
                          validate: checkMail,
                          required: "Email required",
                        })}
                      />
                    </label>
                  </div>

                  <div className={styles.form_field_width_brick}>
                    <label className={styles.form__label}>
                      Confirm Email
                      <input
                        type="email"
                        placeholder="confirm-email@email.com"
                        name="confirmEmail"
                        className={styles.form__text}
                        {...register("confirmEmail", {
                          required: "Configrm Email required",
                          validate: {
                            matchesPreviousMail: (value) => {
                              const { email } = getValues();
                              return email === value || "Emails should match!";
                            },
                          },
                        })}
                      />
                    </label>
                  </div>
                </div>

                <p className={styles.form__field_error}>{emailError()}</p>
              </div>

              <div className={styles.form_field__container}>
                <div className={styles.form_field_width}>
                  <div className={styles.form_field_width_brick}>
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
                  </div>
                  <div className={styles.form_field_width_brick}>
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
                  </div>
                </div>
                <p className={styles.form__field_error}>{passwordError()}</p>
              </div>
              <input type="submit" className={styles.form__submit} />
            </form>

            <div className={styles.form__back_error}>
              {errorMessage ? `Ошибка: ${errorMessage}` : ""}
            </div>
          </div>
        ) : (
          <div className={styles.form}>
            Вы успешно зарегестрированы!
            <br />
            Письмо для подтверждения почты выслано на указанный вами Email
          </div>
        )}
        <GreetingsFooter />
      </div>
    </GreetingsContainer>
  );
}
