import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { HeroUIProvider } from "@heroui/react";
import { RouterProvider } from "react-router-dom";
import routers from "@/routers/pages";
import RequiredTelegram from "./providers/RequiredTelegram";
import { AuthProvider } from "./providers/AuthProvider";

const queryClient = new QueryClient();

const App = () => {
  return (
    <RequiredTelegram>
      <AuthProvider>
        <HeroUIProvider>
          <QueryClientProvider client={queryClient}>
            <TooltipProvider>
              <Toaster />
              <Sonner />
              <RouterProvider router={routers} />
            </TooltipProvider>
          </QueryClientProvider>
        </HeroUIProvider>
      </AuthProvider>
    </RequiredTelegram>
  );
};

export default App;
