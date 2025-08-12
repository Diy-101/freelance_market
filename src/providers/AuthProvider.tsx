import { useState, useEffect, createContext, useContext } from "react";
import { Spinner } from "@telegram-apps/telegram-ui";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const SignIn = async () => {
      try {
        const response = await fetch(`${BASE_URL}/api/auth/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            init_data: window.Telegram.WebApp.initData,
          }),
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

    SignIn();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center">
        <Spinner size="m" />
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ userData }}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
