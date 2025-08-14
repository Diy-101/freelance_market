import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { RouterProvider } from "react-router-dom";
import Providers from "@/providers/providers";
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
