import { createBrowserRouter } from "react-router-dom";
import Index from "@/pages/Index";
import Feed from "@/pages/Feed";
import Search from "@/pages/Search";
import CreateOrder from "@/pages/CreateOrder";
import MyJobs from "@/pages/MyJobs";
import NotFound from "@/pages/NotFound";
import Profile from "@/pages/NewProfile";

const routers = createBrowserRouter([
  {
    path: "/",
    element: <Index />,
  },
  {
    path: "/feed",
    element: <Feed />,
  },
  {
    path: "/search",
    element: <Search />,
  },
  {
    path: "/create",
    element: <CreateOrder />,
  },
  {
    path: "/jobs",
    element: <MyJobs />,
  },
  {
    path: "/profile",
    element: <Profile />,
  },
  {
    path: "*",
    element: <NotFound />,
  },
]);

export default routers;
