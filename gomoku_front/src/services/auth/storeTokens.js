import { TOKEN_LOCAL_STORAGE } from 'services/constants';

export function storeTokens(tokens) {
  localStorage.setItem(TOKEN_LOCAL_STORAGE.tokens, JSON.stringify(tokens));
}

export function storeAcceessToken(accessToken, refreshToken) {
  localStorage.setItem(
    TOKEN_LOCAL_STORAGE.tokens,
    JSON.stringify({
      access_token: accessToken,
      refresh_token: refreshToken,
    }),
  );
}

export function deleteTokens() {
    localStorage.removeItem(TOKEN_LOCAL_STORAGE.tokens);
}
