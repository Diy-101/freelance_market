import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import RequiredTelegram from "@/providers/RequiredTelegram";
import { AuthProvider } from "@/providers/AuthProvider";
import { HeroUIProvider } from "@heroui/react";
export const Providers = ({ children }) => {
  const queryClient = new QueryClient();
  return (
    <HeroUIProvider>
      <RequiredTelegram>
        <AuthProvider>
          <QueryClientProvider client={queryClient}>
            <TooltipProvider>{children}</TooltipProvider>
          </QueryClientProvider>
        </AuthProvider>
      </RequiredTelegram>
    </HeroUIProvider>
  );
};

export default Providers;
