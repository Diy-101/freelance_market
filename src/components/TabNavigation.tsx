import { useLocation, useNavigate } from "react-router-dom";
import { Home, Search, Plus, User, Briefcase } from "lucide-react";

const tabs = [
  { icon: Home, label: "Feed", path: "/feed" },
  { icon: Search, label: "Search", path: "/search" },
  { icon: Plus, label: "Create", path: "/create" },
  { icon: Briefcase, label: "My Jobs", path: "/jobs" },
  { icon: User, label: "Profile", path: "/profile" },
];

export const TabNavigation = () => {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <div className="fixed bottom-3 left-0 right-0 z-50 flex justify-center">
      <div
        className="flex justify-around items-center gap-6 rounded-full px-6 py-3
                      bg-white/80 dark:bg-gray-900/70 backdrop-blur-lg
                      border-2 border-primary/70 shadow-xl max-w-md w-full"
      >
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = location.pathname === tab.path;

          return (
            <button
              key={tab.path}
              onClick={() => navigate(tab.path)}
              className={`relative flex flex-col items-center text-xs font-medium transition-colors
                          ${
                            isActive ? "text-primary" : "text-muted-foreground"
                          }`}
            >
              <Icon size={22} className="mb-1" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
