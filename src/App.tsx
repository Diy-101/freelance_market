import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import Providers from "./providers/providers";
import { RouterProvider } from "react-router-dom";
import routers from "@/routers/pages";

const App = () => {
  return (
    <Providers>
      <Toaster />
      <Sonner />
      <RouterProvider router={routers} />
    </Providers>
  );
};

export default App;
