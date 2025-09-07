import { useLocation, useNavigate } from "react-router-dom";
import {
  HouseIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  BriefcaseIcon,
  UserIcon,
} from "@phosphor-icons/react";
import { motion } from "framer-motion";
import useAuth from "@/hooks/useAuth";
import { text } from "stream/consumers";

const tabs = [
  { icon: HouseIcon, label: "Feed", path: "/feed" },
  { icon: MagnifyingGlassIcon, label: "Search", path: "/search" },
  { icon: PlusIcon, label: "Create", path: "/create", special: true },
  { icon: BriefcaseIcon, label: "My Jobs", path: "/jobs" },
];

export const TabNavigation = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <div className="fixed bottom-3 left-0 right-0 z-50 flex justify-center">
      <div
        className="flex justify-around items-center gap-4 rounded-full px-4 py-2
                   bg-white/90 dark:bg-gray-900/80 backdrop-blur-lg
                   border border-gray-200 dark:border-gray-700
                   shadow-lg max-w-sm w-full"
      >
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = location.pathname === tab.path;

          if (tab.special) {
            return (
              <motion.button
                key={tab.path}
                onClick={() => navigate(tab.path)}
                className="flex items-center justify-center rounded-full
                           bg-primary text-white shadow-lg
                           w-14 h-14 -mt-8"
                whileTap={{ scale: 0.9 }}
                whileHover={{ scale: 1.1 }}
              >
                <Icon size={28} />
              </motion.button>
            );
          }

          return (
            <motion.button
              key={tab.path}
              onClick={() => navigate(tab.path)}
              className={`relative flex flex-col items-center text-xs font-medium transition-colors
                          ${
                            isActive ? "text-primary" : "text-muted-foreground"
                          }`}
              whileTap={{ scale: 0.9 }}
            >
              <Icon size={22} className="mb-1" />
              <span>{tab.label}</span>
            </motion.button>
          );
        })}
        <motion.button
          key={"/profile"}
          onClick={() => navigate("/profile")}
          className={`relative flex flex-col items-center text-xs font-medium transition-colors
                          ${
                            location.pathname == "/profile"
                              ? "text-primary"
                              : "text-muted-foreground"
                          }`}
          whileTap={{ scale: 0.9 }}
        >
          <img
            src={user?.photo_url}
            alt={user.firstName}
            className={`w-6 h-6 mb-1 object-cover rounded-full border-2 border-gray-300 ${
              location.pathname == "/profile"
                ? "text-primary"
                : "text-muted-foreground"
            }`}
          />
          <span>Profile</span>
        </motion.button>
      </div>
    </div>
  );
};
