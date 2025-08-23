export interface Card {
  title: string;
  description: string;
  button: string;
}

export interface LanguageTranslations {
  onboarding: Card[];
}

export interface Translations {
  ru: LanguageTranslations;
}

export const translations: Translations = {
  ru: {
    onboarding: [
      {
        title: "Найди лучших исполнителей",
        description:
          "Свяжись с профессионалами своего дела и выбери того, кто подходит именно тебе. Изучай отзывы, оценки, компетенции, перки и делай свой выбор.",
        button: "Дальше",
      },
      {
        title: "Быстро & Эффективно",
        description:
          "Получи выполненный проект быстро с помощью налаженного процесса подбора релевантных специалистов. С помощью одной кнопки приложение подберет самых подходящих исполнителей.",
        button: "Дальше",
      },
      {
        title: "Комиссия 0%",
        description:
          "Оставляй 100% заработанных денег! А мы позаботимся за об удобстве использования и скорости подбора заказов",
        button: "Начать",
      },
    ],
  },
};
