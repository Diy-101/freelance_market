export default async function authUser(initData) {
  try {
    const response = await fetch(
      "https://1be8efe2be36.ngrok-free.app/api/checkuser",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(initData),
      }
    );
    const initDataJSON = await response.json();
    return initDataJSON;
  } catch (err) {
    console.log("Ошибка при проверке авторизации:", err);
  }
}
