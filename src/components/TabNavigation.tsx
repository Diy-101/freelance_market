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
    <div className="tab-nav fixed bottom-0 left-0 right-0 z-50">
      <div className="flex justify-around items-center max-w-md mx-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = location.pathname === tab.path;
          
          return (
            <button
              key={tab.path}
              onClick={() => navigate(tab.path)}
              className={`tab-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={20} className="mb-1" />
              <span className="text-xs font-medium">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};