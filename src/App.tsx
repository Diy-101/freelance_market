import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { HeroUIProvider } from "@heroui/react";
import { RouterProvider } from "react-router-dom";
import routers from "@/routers/default";

const queryClient = new QueryClient();

const App = () => (
  <HeroUIProvider>
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <RouterProvider router={routers} />
      </TooltipProvider>
    </QueryClientProvider>
  </HeroUIProvider>
);

export default App;
