/* eslint-disable prefer-template */

import { TOKEN_LOCAL_STORAGE } from 'services/constants';

export default function authHeader() {
  // eslint-disable-next-line no-undef
  const tokens = JSON.parse(localStorage.getItem(TOKEN_LOCAL_STORAGE.tokens));

  if (tokens && tokens.access_token) {
    return { Authorization: 'Bearer ' + tokens[TOKEN_LOCAL_STORAGE.accessToken] };
  }
  return {};
}

export function refreshHeader() {
  // eslint-disable-next-line no-undef
  const tokens = JSON.parse(localStorage.getItem(TOKEN_LOCAL_STORAGE.tokens));

  if (tokens && tokens.access_token) {
    return { Authorization: 'Bearer ' + tokens[TOKEN_LOCAL_STORAGE.refreshToken] };
  }
  return {};
}
