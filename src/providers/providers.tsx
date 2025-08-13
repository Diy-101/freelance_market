import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import RequiredTelegram from "@/providers/RequiredTelegram";
import { AuthProvider } from "@/providers/AuthProvider";
import { AppRoot } from "@telegram-apps/telegram-ui";

export const Providers = ({ children }) => {
  const queryClient = new QueryClient();
  return (
    <AppRoot>
      <RequiredTelegram>
        <AuthProvider>
          <QueryClientProvider client={queryClient}>
            <TooltipProvider>{children}</TooltipProvider>
          </QueryClientProvider>
        </AuthProvider>
      </RequiredTelegram>
    </AppRoot>
  );
};

export default Providers;
