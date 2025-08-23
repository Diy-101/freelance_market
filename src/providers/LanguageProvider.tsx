import { createContext, useState, ReactNode } from "react";
import { translations } from "@/lib/translations";
import type { LanguageTranslations } from "@/lib/translations";

interface LanguageContextType {
  language: string;
  setLanguage: (lang: string) => void;
  t: () => LanguageTranslations;
}

export const LanguageContext = createContext<LanguageContextType | null>(null);

export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLanguage] = useState("ru");

  const t = () => translations[language];

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};
