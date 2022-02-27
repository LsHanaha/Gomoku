import { getQueries } from "services/apiQueries";
import { TOKEN_LOCAL_STORAGE, BACKEND_ENDPOINTS } from "services/constants";

export default async function checkAuthentication() {
  // eslint-disable-next-line no-undef
  const token = JSON.parse(localStorage.getItem(TOKEN_LOCAL_STORAGE.tokens));

  if (!token || !token.access_token) {
    return new Promise((resolve) => resolve({ status: false }));
  }

  try {
    const currentUser = await getQueries(
      `${BACKEND_ENDPOINTS.auth}${BACKEND_ENDPOINTS.me}`
    );

    if (!currentUser.status === 200) {
      return new Promise((resolve) => resolve({ status: false }));
    }
    return new Promise((resolve) => resolve({ status: true }));
  } catch (error) {
    return new Promise((resolve) => resolve({ status: false }));
  }
}
