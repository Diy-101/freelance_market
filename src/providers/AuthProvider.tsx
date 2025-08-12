import { useState, useEffect, createContext, useContext } from "react";
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [userData, setUserData] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    window.Telegram?.WebApp?.ready();

    const trySignIn = async () => {
      const initData = window.Telegram?.WebApp?.initData || "";
      console.log("Init data received:", initData);

      if (!initData) {
        console.warn(
          "⚠️ Init data is empty. Check how the app is opened in Telegram."
        );
        setLoading(false);
        return;
      }

      try {
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
        setToken(data.access_token);
      } catch (error) {
        console.error("Auth error:", error);
        setUserData(null);
      } finally {
        setLoading(false);
      }
    };

    // Иногда на мобильном initData появляется с задержкой
    const timer = setTimeout(trySignIn, 300);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (!userData) {
    return (
      <div>
        Ошибка авторизации. Пожалуйста, откройте приложение из Telegram.
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ userData, token }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
