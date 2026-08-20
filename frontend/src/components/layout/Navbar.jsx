import { Link, useLocation } from "react-router-dom";
import { FaBrain } from "react-icons/fa";
import "../../styles/Navbar.css";

function Navbar() {
  const location = useLocation();

  return (
    <nav className="navbar">
      <Link to="/" className="logo">
        <FaBrain className="logo-icon" />
        <span>MindSync AI</span>
      </Link>

      <ul className="nav-links">
        <li>
          <Link
            to="/"
            className={location.pathname === "/" ? "active" : ""}
          >
            Home
          </Link>
        </li>

        <li>
          <Link
            to="/about"
            className={location.pathname === "/about" ? "active" : ""}
          >
            About
          </Link>
        </li>

        <li>
          <Link
            to="/login"
            className={location.pathname === "/login" ? "active" : ""}
          >
            Login
          </Link>
        </li>

        <li>
          <Link
            to="/signup"
            className={location.pathname === "/signup" ? "active" : ""}
          >
            Signup
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;