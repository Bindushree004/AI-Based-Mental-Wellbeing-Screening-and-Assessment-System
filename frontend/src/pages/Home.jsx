import { useNavigate } from "react-router-dom";

import Hero from "../components/home/Hero";
import Features from "../components/home/Features";
import HowItWorks from "../components/home/HowItWorks";
import Statistics from "../components/home/Statistics";
import FAQ from "../components/home/FAQ";
import CallToAction from "../components/home/CallToAction";

import "./Home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-page">

      {/* ================================
          TOP NAVIGATION BAR
      ================================= */}

      <nav className="home-navbar">

        {/* Logo */}
        <div className="home-logo">

          <div className="home-logo-icon">
            🧠
          </div>

          <div className="home-logo-text">
            <h2>MindSync AI</h2>
          </div>

        </div>


        {/* Login / Signup */}
        <div className="home-nav-links">

          <button
            type="button"
            className="home-login-btn"
            onClick={() => navigate("/login")}
          >
            Login
          </button>

          <button
            type="button"
            className="home-signup-btn"
            onClick={() => navigate("/signup")}
          >
            Sign Up
          </button>

        </div>

      </nav>


      {/* ================================
          HOME SECTIONS
      ================================= */}

      <Hero />

      <Features />

      <HowItWorks />

      <Statistics />

      <FAQ />

      <CallToAction />

    </div>
  );
}

export default Home;