import { useState, useEffect, createContext, useContext } from "react";
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [userData, setUserData] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const signIn = async (initData: string) => {
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
        setUserData(null);
        console.error(error);
      }
    };

    signIn(window.Telegram.WebApp.initData);
  }, []);

  if (userData === null) {
    return <div>Загрузка...</div>;
  }

  return (
    <AuthContext.Provider value={{ userData, token }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = useContext(AuthContext);
