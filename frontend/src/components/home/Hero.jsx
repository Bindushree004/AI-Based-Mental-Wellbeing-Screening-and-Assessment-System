import "../../styles/Hero.css";
import { Link } from "react-router-dom";
import heroImage from "../../images/hero-image.png";

function Hero() {
  return (
    <section className="hero">

      {/* Watermark Background Image */}
      <img
        src={heroImage}
        alt=""
        className="hero-watermark"
      />

      <div className="hero-content">

        <h1>
          AI-Based Mental Wellbeing
          <br />
          Screening &
          <span> Assessment System</span>
        </h1>

        <div className="hero-line"></div>

        <p>
          Empowering individuals with AI-driven mental wellbeing
          screening, personalized insights, and early emotional
          wellness assessment.
        </p>

        <div className="hero-buttons">

          <Link to="/signup" className="primary-btn">
            Start Assessment
          </Link>

          <Link to="/about" className="secondary-btn">
            Learn More
          </Link>

        </div>

      </div>

    </section>
  );
}

export default Hero;