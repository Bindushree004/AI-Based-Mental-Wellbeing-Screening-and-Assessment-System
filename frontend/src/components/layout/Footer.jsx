import { Link } from "react-router-dom";
import {
  FaGithub,
  FaLinkedin,
  FaInstagram,
  FaEnvelope,
  FaMapMarkerAlt,
  FaPhone,
} from "react-icons/fa";

import "../../styles/Footer.css";

function Footer() {
  return (
    <footer className="footer">

      <div className="footer-container">

        <div className="footer-column">

          <h2>🧠 MindSync AI</h2>

          <p>
            AI-powered mental wellbeing screening and assessment
            platform helping individuals monitor, understand,
            and improve their emotional wellbeing using
            Artificial Intelligence.
          </p>

        </div>

        <div className="footer-column">

          <h3>Quick Links</h3>

          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <Link to="/login">Login</Link>
          <Link to="/signup">Signup</Link>

        </div>

        <div className="footer-column">

          <h3>Resources</h3>

          <a href="#">Privacy Policy</a>
          <a href="#">Terms & Conditions</a>
          <a href="#">FAQ</a>

        </div>

        <div className="footer-column">

          <h3>Contact</h3>

          <p><FaEnvelope /> support@mindsync.ai</p>

          <p><FaMapMarkerAlt /> Mysuru, Karnataka</p>

          <p><FaPhone /> +91 XXXXX XXXXX</p>

        </div>

      </div>

      <div className="social-icons">

        <a href="#"><FaGithub /></a>

        <a href="#"><FaLinkedin /></a>

        <a href="#"><FaInstagram /></a>

      </div>

      <hr />

      <div className="copyright">

        © 2026 MindSync AI. All Rights Reserved.

      </div>

    </footer>
  );
}

export default Footer;