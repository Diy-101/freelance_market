import { createContext } from "react";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { HeroUIProvider } from "@heroui/react";
import { RouterProvider } from "react-router-dom";
import routers from "@/routers/pages";
import { useTelegramAuth } from "./hooks/useTelegramAuth";

const queryClient = new QueryClient();
const UserContext = createContext(null);

const App = () => {
  const user = useTelegramAuth();

  return (
    <UserContext.Provider value={user}>
      <HeroUIProvider>
        <QueryClientProvider client={queryClient}>
          <TooltipProvider>
            <Toaster />
            <Sonner />
            <RouterProvider router={routers} />
          </TooltipProvider>
        </QueryClientProvider>
      </HeroUIProvider>
    </UserContext.Provider>
  );
};

export default App;
