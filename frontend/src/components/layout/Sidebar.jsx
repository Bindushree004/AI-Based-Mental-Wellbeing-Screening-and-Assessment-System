import { NavLink, useNavigate } from "react-router-dom";

import {
  FaHome,
  FaClipboardCheck,
  FaHistory,
  FaLightbulb,
  FaUser,
  FaSignOutAlt,
  FaBrain,
} from "react-icons/fa";

import "./Sidebar.css";

function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <aside className="sidebar">

      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <FaBrain />
        </div>

        <h2>MindSync AI</h2>
      </div>

      <nav className="sidebar-navigation">

        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            isActive ? "sidebar-link active" : "sidebar-link"
          }
        >
          <FaHome />
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/assessment"
          className={({ isActive }) =>
            isActive ? "sidebar-link active" : "sidebar-link"
          }
        >
          <FaClipboardCheck />
          <span>Assessment</span>
        </NavLink>

        <NavLink
          to="/history"
          className={({ isActive }) =>
            isActive ? "sidebar-link active" : "sidebar-link"
          }
        >
          <FaHistory />
          <span>Assessment History</span>
        </NavLink>

        <NavLink
          to="/recommendations"
          className={({ isActive }) =>
            isActive ? "sidebar-link active" : "sidebar-link"
          }
        >
          <FaLightbulb />
          <span>Recommendations</span>
        </NavLink>

        <NavLink
          to="/profile"
          className={({ isActive }) =>
            isActive ? "sidebar-link active" : "sidebar-link"
          }
        >
          <FaUser />
          <span>My Profile</span>
        </NavLink>

      </nav>

      <div className="sidebar-bottom">
        <button
          type="button"
          className="sidebar-logout"
          onClick={handleLogout}
        >
          <FaSignOutAlt />
          <span>Logout</span>
        </button>
      </div>

    </aside>
  );
}

export default Sidebar;