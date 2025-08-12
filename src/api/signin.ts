export default async function signIn(initData: string) {
  try {
    const response = await fetch(
      "https://22d0962b5aec.ngrok-free.app/api/auth/signin",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ init_data: initData }),
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
