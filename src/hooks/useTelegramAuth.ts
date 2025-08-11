import { useState, useEffect } from "react";
import authUser from "@/api/auth";

export const useTelegramAuth = () => {
  const initData = window.Telegram.WebApp.initData;
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const validUserData = await authUser(initData);
        setUserData(validUserData);
      } catch (err) {
        console.log("Ошибка при проверке авторизации:", err);
      }
    };

    fetchData();
  }, []);

  return userData;
};
