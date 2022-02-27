// /* eslint-disable import/prefer-default-export */

import React, { useState, useEffect } from "react";
import { useLocation, useHistory, Link } from "react-router-dom";

import { GreetingsFooter } from "components/greetingsFooter";
import { GreetingsContainer } from "components/greetingsContainer/GreetingsContainer";

import { postQueries } from "services/apiQueries";
import { ROUTER_ENDPOINTS, BACKEND_ENDPOINTS } from "services/constants";

import styles from "./EmailVerificationPage.module.css";

export function VerifyEmailPage() {
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setNewSuccessMessage] = useState("");
  const history = useHistory();
  const { search } = useLocation();

  useEffect(() => {
    const query = async () => {
      const isTokenValid = await checkToken();
      if (isTokenValid) {
        const id = setTimeout(() => {
          history.push(ROUTER_ENDPOINTS.signIn);
        }, 3000);
        return () => {
          clearTimeout(id);
        };
      }
    };

    query();
  }, []);

  const checkToken = async () => {
    const token = new URLSearchParams(search).get("token");
    try {
      const response = await postQueries(
        `${BACKEND_ENDPOINTS.auth}${BACKEND_ENDPOINTS.emailVerification}`,
        { token }
      );
      if (response.status === 201) return true;
    } catch (error) {
      setErrorMessage(JSON.parse(error.message).detail);
    }

    return false;
  };

  return (
    <GreetingsContainer>
      <div className={styles.page_container_header}>
        <Link to={ROUTER_ENDPOINTS.greetings} className={styles.page_label}>
          Gomoku
        </Link>
      </div>
      <div className={styles.form}>
        <div>
          {successMessage
            ? { successMessage }
            : "Идет верификация учетной записи"}
        </div>
        <div className={styles.form__field_error}>
          {errorMessage ? `Ошибка: ${errorMessage}` : ""}
        </div>
      </div>
      <GreetingsFooter />
    </GreetingsContainer>
  );
}
