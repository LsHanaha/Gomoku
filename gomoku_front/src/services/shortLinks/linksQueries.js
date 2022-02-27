import axios from "axios";
import { TOKEN_LOCAL_STORAGE } from "services/constants";
import authHeader from "services/auth/authHeaders";

import { parseJwt } from "services/auth/parseJwt";

const axiosApiInstance = axios.create({
  baseURL: "http://51.250.30.11:8089",
  // baseURL: "http://localhost:3001",
});

export const getLinks = async (endpoint, params = null) => {
  const tokens = JSON.parse(localStorage.getItem(TOKEN_LOCAL_STORAGE.tokens));

  const userId = parseJwt(tokens.access_token).sub;

  const config = params
    ? { headers: authHeader(), params: params }
    : { headers: authHeader() };

  endpoint = `${endpoint}?accountId=${userId}`;

  try {
    const response = await axiosApiInstance.get(endpoint, config);
    return response.data;
  } catch (error) {
    throw new Error(JSON.stringify(error.response.data));
  }
};

export const postLinks = async (endpoint, postParams) => {
  try {
    const response = await axiosApiInstance.post(endpoint, postParams, {
      headers: authHeader(),
    });

    return response;
  } catch (error) {
    throw new Error(error.message);
  }
};

export const updateLinks = async (endpoint, putParams) => {
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

export const deleteLinks = async (endpoint, deleteParams) => {
  // TODO я так и не увидел тело запроса на удаление

  try {
    const response = await axiosApiInstance.delete(endpoint, {
      headers: authHeader(),
      data: deleteParams,
    });

    return response;
  } catch (error) {
    throw new Error(error?.message);
  }
};
