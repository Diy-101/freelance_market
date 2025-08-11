import { useState, useEffect } from "react";
import authUser from "@/api/auth";

export const useTelegramAuth = () => {
  const initData = window.Telegram.WebApp.initData;
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const validUserData = await authUser(initData);
      setUserData(validUserData);
    };

    fetchData();
  }, []);

  return userData;
};
