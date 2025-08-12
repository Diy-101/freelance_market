import { useState, useEffect, createContext, useContext } from "react";
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    window.Telegram?.WebApp?.ready();

    const trySignIn = async () => {
      try {
        // Проверяем наличие initData
        const initData = window.Telegram?.WebApp?.initData;

        if (!initData) {
          throw new Error("No initData available");
        }

        const response = await fetch(`${BASE_URL}/api/auth/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ init_data: initData }),
        });

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

    // Ждем немного, пока WebApp полностью инициализируется
    const checkInitData = () => {
      let attempts = 0;
      const maxAttempts = 10;

      const check = () => {
        const initData = window.Telegram?.WebApp?.initData;

        if (initData) {
          trySignIn();
        } else if (attempts < maxAttempts) {
          attempts++;
          setTimeout(check, 300);
        } else {
          console.error("Init data not available after multiple attempts");
          setLoading(false);
        }
      };

      check();
    };

    checkInitData();
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
