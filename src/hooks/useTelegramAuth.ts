import { useState } from "react";
import signIn from "@/api/signin";

export const useTelegramAuth = () => {
  const [userData, setUserData] = useState(null);

  const auth = async (initData: string) => {
    const res = await signIn(initData);
    setUserData(res);
  };

  return { userData, auth };
};
