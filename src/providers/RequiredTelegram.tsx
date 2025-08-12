import React from "react";

export default function RequiredTelegram({ children }) {
  window.Telegram?.WebApp?.ready();
  const tg = window.Telegram?.WebApp;
  const isTelegram = tg && tg.initData;

  if (!isTelegram) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 text-center p-6">
        <div className="max-w-md bg-white rounded-2xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Это приложение работает только внутри Telegram
          </h2>
          <p className="text-gray-600 mb-6">
            Пожалуйста, откройте его через нашего бота:
          </p>
          <a
            href="https://t.me/your_bot_username/startapp"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-[#0088cc] hover:bg-[#0077b6] text-white font-medium py-3 px-6 rounded-lg shadow-md transition"
          >
            🚀 Запустить в Telegram
          </a>
        </div>
      </div>
    );
  }

  return children;
}
