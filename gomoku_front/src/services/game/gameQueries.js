import axios from "axios";
import {GAME_ENDPOINTS, BASE_URL, TOKEN_LOCAL_STORAGE} from "services/constants";
import authHeader from "services/auth/authHeaders";

import { parseJwt } from "services/auth/parseJwt";

const axiosApiInstance = axios.create({
    baseURL: `${BASE_URL.baseProtocol}://${BASE_URL.baseHost}:${BASE_URL.basePort}/${GAME_ENDPOINTS.prefix}`,
});


export const getQueries = async (endpoint, params= null) => {
    const config = params
      ? { headers: authHeader(), params: params }
      : { headers: authHeader() };

    try {
        const response = await axiosApiInstance.get(endpoint, config);
        return response.data;
    } catch (error) {
        throw new Error(JSON.stringify(error.response.data));
    }
}


export const postQueries = async (endpoint, postParams) => {
    try {
        const response = await axiosApiInstance.post(endpoint, postParams, {
            headers: authHeader(),
        });

        return response;
    } catch (error) {
        throw new Error(JSON.stringify(error.response?.data));
    }
}
