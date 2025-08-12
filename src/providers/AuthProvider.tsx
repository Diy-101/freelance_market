import { useState, useEffect, createContext, useContext } from "react";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const SignIn = async () => {
      try {
        // Проверяем наличие initData
        const initData = window.Telegram.WebApp.initData;

        if (!initData) {
          throw new Error("No initData available");
        }

        const response = await fetch(
          `https://22d0962b5aec.ngrok-free.app/api/auth/login`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ init_data: initData }),
          }
        );

        if (!response.ok)
          throw new Error(`HTTP request Error: ${response.status}`);

        const data = await response.json();
        setUserData(data.user);
        localStorage.setItem("token", data.access_token);
      } catch (error) {
        setUserData(null);
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    SignIn();
  }, []);

  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        Загрузка...
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ userData }}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
