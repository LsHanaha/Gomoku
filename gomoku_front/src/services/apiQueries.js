/* import {history} from '../services/history'; */
/* eslint no-underscore-dangle: 0 */
/* eslint-disable camelcase */

import axios from "axios";

import authHeader, { refreshHeader } from "services/auth/authHeaders";
import { storeAcceessToken } from "services/auth/storeTokens";
import { TOKEN_LOCAL_STORAGE, BACKEND_ENDPOINTS } from "services/constants";

const axiosApiInstance = axios.create({
  baseURL: "http://51.250.104.143:8888",
});

async function refreshToken() {
  const tokens = JSON.parse(localStorage.getItem(TOKEN_LOCAL_STORAGE.tokens));

  const response = await axiosApiInstance.post(
    `${BACKEND_ENDPOINTS.auth}${BACKEND_ENDPOINTS.refresh}`,
    { refresh_token: tokens.refresh_token },
    { headers: refreshHeader() }
  );
  if (response.status === 200) {
    storeAcceessToken(
      response.data[TOKEN_LOCAL_STORAGE.accessToken],
      tokens[TOKEN_LOCAL_STORAGE.refreshToken]
    );
    return response.data[TOKEN_LOCAL_STORAGE.accessToken];
  }
  throw new Error("Token not available");
}

axiosApiInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const originalResponse = error;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const accessToken = await refreshToken();
        originalRequest.headers.Authorization = `Bearer ${accessToken}`;
        return axiosApiInstance(originalRequest);
      } catch {
        throw originalResponse;
      }
    }
    return Promise.reject(error);
  }
);

export const getQueries = async (endpoint, getParams = null) => {
  const config = getParams
    ? { headers: authHeader(), params: getParams }
    : { headers: authHeader() };

  try {
    const response = await axiosApiInstance.get(endpoint, config);
    return response;
  } catch (error) {
    throw new Error(JSON.stringify(error.response.data));
  }
};

export const postQueries = async (endpoint, postParams) => {
  try {
    const response = await axiosApiInstance.post(endpoint, postParams, {
      headers: authHeader(),
    });

    return response;
  } catch (error) {
    throw new Error(JSON.stringify(error.response?.data));
  }
};

export const updateQueries = async (endpoint, putParams) => {
  try {
    const response = await axiosApiInstance.put(
      endpoint,
      { data: putParams },
      { headers: authHeader() }
    );

    return response;
  } catch (error) {
    throw new Error(JSON.stringify(error.response.data));
  }
};

export const deleteQueries = async (endpoint, deleteParams) => {
  const config = deleteParams
    ? { headers: authHeader(), params: deleteParams }
    : { headers: authHeader() };

  try {
    const response = await axiosApiInstance.delete(endpoint, config);

    return response;
  } catch (error) {
    throw new Error(error.response.data);
  }
};
