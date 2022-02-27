export const BACKEND_ENDPOINTS = {
  auth: '/auth',
  signIn: '/signin',
  signUp: '/signup',
  refresh: '/refresh',
  me: '/me',
  emailVerification: '/email-verification',
  restorePassword: '/restore-password',
  newPassword: '/new-password',
  accessRevoke: '/access-revoke',
  refreshRevoke: '/refresh-revoke',
};

export const ROUTER_ENDPOINTS = {
  greetings: '/',
  home: '/home',
  signIn: '/sign-in',
  signUp: '/sign-up',
  emailVerification: '/email-verification',
  restoreMail: '/restore-mail',
  restorePwd: '/restore-password',
  newPassword: '/new-password',
  history: '/history',
  newGame: '/new-game',
  game: '/game'
};

export const TOKEN_LOCAL_STORAGE = {
  accessToken: 'access_token',
  refreshToken: 'refresh_token',
  tokens: 'tokens',
};

export const GAME_LOCAL_STORAGE = {
  uuid: 'uuid'
}

export const GAME_ENDPOINTS = {
  prefix: "game/",
  startGame: '',
  checkStored: 'check-stored/',
  newGame: 'new-game/'
}

export const BASE_URL = {
  baseHost: "0.0.0.0",
  basePort: "8888",
  baseProtocol: "http"
}
