import "../../styles/Features.css";

import {
  FaBrain,
  FaClipboardCheck,
  FaLightbulb,
  FaChartLine,
  FaShieldAlt,
  FaBolt,
} from "react-icons/fa";

function Features() {
  const features = [
    {
      icon: <FaBrain />,
      title: "AI-Powered Analysis",
      description:
        "Advanced machine learning models analyze your responses to identify mental wellbeing patterns.",
    },
    {
      icon: <FaClipboardCheck />,
      title: "Comprehensive Assessment",
      description:
        "Scientifically designed questionnaires help evaluate stress, anxiety, and depression levels.",
    },
    {
      icon: <FaLightbulb />,
      title: "Personalized Recommendations",
      description:
        "Receive tailored suggestions that encourage healthier habits and emotional wellbeing.",
    },
    {
      icon: <FaChartLine />,
      title: "Progress Tracking",
      description:
        "Monitor your mental wellbeing journey through your previous assessment history.",
    },
    {
      icon: <FaShieldAlt />,
      title: "Privacy & Security",
      description:
        "Your personal information and assessment results are stored securely and confidentially.",
    },
    {
      icon: <FaBolt />,
      title: "Fast & User Friendly",
      description:
        "Complete assessments quickly with a clean, responsive, and intuitive interface.",
    },
  ];

  return (
    <section className="features-section">

      <h2>Why Choose MindSync AI?</h2>

      <p className="feature-subtitle">
        Discover how artificial intelligence empowers mental wellbeing through
        secure assessments, personalized insights, and meaningful progress
        tracking.
      </p>

      <div className="feature-grid">
        {features.map((feature, index) => (
          <div className="feature-card" key={index}>

            <div className="feature-icon">
              {feature.icon}
            </div>

            <h3>{feature.title}</h3>

            <p>{feature.description}</p>

          </div>
        ))}
      </div>

    </section>
  );
}

export default Features;