import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { useEffect } from "react";
import { RouterProvider } from "react-router-dom";
import Providers from "@/providers/providers";
import routers from "@/routers/pages";

const App = () => {
  useEffect(() => {
    const handleWheel = (e: WheelEvent) => {
      if (e.ctrlKey) e.preventDefault(); // блокируем масштаб через Ctrl + колесо
    };

    const handleKey = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && ["+", "-", "="].includes(e.key)) {
        e.preventDefault(); // блокируем Ctrl+/Ctrl- (или Cmd на Mac)
      }
    };

    window.addEventListener("wheel", handleWheel, { passive: false });
    window.addEventListener("keydown", handleKey);

    return () => {
      window.removeEventListener("wheel", handleWheel);
      window.removeEventListener("keydown", handleKey);
    };
  }, []);

  return (
    <Providers>
      <Toaster />
      <Sonner />
      <RouterProvider router={routers} />
    </Providers>
  );
};

export default App;
