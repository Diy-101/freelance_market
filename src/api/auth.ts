export default async function authUser(initData) {
  const response = await fetch(
    "https://1be8efe2be36.ngrok-free.app/api/checkuser",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(initData),
    }
  ).catch(console.error);

  const initDataJSON = await response.json();
  return initDataJSON;
}
