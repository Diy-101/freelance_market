export default async function signIn(initData: string) {
  try {
    const response = await fetch(
      "https://2fd83bcd4890.ngrok-free.app/api/auth/signin",
      {
        method: "POST",
        headers: {
          "Content-Type": "text/plain",
        },
        body: initData,
      }
    );

    if (!response.ok) {
      throw new Error("Auth failed");
    }

    const initDataJSON = await response.json();
    localStorage.setItem("access_token", initDataJSON.access_token);
    localStorage.setItem("refresh_token", initDataJSON.refresh_token);

    return initDataJSON.user;
  } catch (err) {
    console.log("Ошибка при проверке авторизации:", err);
  }
}
