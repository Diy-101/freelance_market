import React from "react";

export default function RequiredTelegram({ children }) {
  const _ = window.Telegram.WebApp.ready();
  const isTelegram = window.Telegram?.WebApp.initData ? false : true;

  if (!isTelegram) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-background text-foreground p-6">
        <div className="telegram-card max-w-md text-center">
          <h2 className="text-2xl font-bold mb-4">
            Это приложение работает только внутри Telegram
          </h2>
          <p className="mb-6">Пожалуйста, откройте его через нашего бота:</p>
          <a
            href="https://t.me/your_bot_username/startapp"
            target="_blank"
            rel="noopener noreferrer"
            className="telegram-button inline-block"
          >
            🚀 Запустить в Telegram
          </a>
        </div>
      </div>
    );
  }

  return children;
}
