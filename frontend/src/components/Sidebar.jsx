import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  ClipboardCheck,
  History,
  Lightbulb,
  User,
  LogOut,
} from "lucide-react";

import "./Sidebar.css";

function Sidebar() {
  const menuItems = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      name: "Assessment",
      path: "/assessment",
      icon: ClipboardCheck,
    },
    {
      name: "Assessment History",
      path: "/history",
      icon: History,
    },
    {
      name: "Recommendations",
      path: "/recommendations",
      icon: Lightbulb,
    },
    {
      name: "My Profile",
      path: "/profile",
      icon: User,
    },
  ];

  return (
    <aside className="sidebar">

      {/* Logo */}
      <div className="sidebar-logo">
        <div className="logo-icon">🧠</div>

        <div>
          <h2>MindSync AI</h2>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-navigation">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive
                  ? "sidebar-link active"
                  : "sidebar-link"
              }
            >
              <Icon size={20} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}

      </nav>

      {/* Logout */}
      <div className="sidebar-bottom">

        <button
          className="sidebar-logout"
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/login";
          }}
        >
          <LogOut size={20} />
          <span>Logout</span>
        </button>

      </div>

    </aside>
  );
}

export default Sidebar;