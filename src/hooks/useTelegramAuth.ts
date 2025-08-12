import { useState } from "react";
const BASE_URL = import.meta.env.BASE_URL;

export const useTelegramAuth = () => {
  const [userData, setUserData] = useState(null);

  const validate = async (initData: string) => {
    try {
      const response = await fetch(`${BASE_URL}/api/auth/validate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ init_data: initData }),
      });

      if (!response.ok)
        throw new Error(`HTTP request Error: ${response.status}`);

      const data = await response.json();
      setUserData(data);
    } catch (error) {
      setUserData(null);
      console.error(error);
    }
  };

  return { userData, validate };
};
