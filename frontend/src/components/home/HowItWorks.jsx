import "../../styles/HowItWorks.css";

import {
  FaUserPlus,
  FaSignInAlt,
  FaClipboardList,
  FaBrain,
  FaChartPie,
  FaLightbulb,
} from "react-icons/fa";

function HowItWorks() {
  const steps = [
    {
      icon: <FaUserPlus />,
      title: "Create Account",
      description: "Register securely to access your personal dashboard.",
    },
    {
      icon: <FaSignInAlt />,
      title: "Login",
      description: "Sign in to continue your mental wellbeing journey.",
    },
    {
      icon: <FaClipboardList />,
      title: "Take Assessment",
      description: "Answer scientifically designed mental wellbeing questions.",
    },
    {
      icon: <FaBrain />,
      title: "AI Analysis",
      description: "Our AI analyzes your responses using machine learning.",
    },
    {
      icon: <FaChartPie />,
      title: "View Results",
      description: "See your wellbeing score and detailed insights.",
    },
    {
      icon: <FaLightbulb />,
      title: "Get Recommendations",
      description: "Receive personalized suggestions for better wellbeing.",
    },
  ];

  return (
    <section className="how-it-works">
      <h2>How It Works</h2>

      <p className="how-subtitle">
        Complete your assessment in six simple steps and receive AI-powered
        mental wellbeing insights.
      </p>

      <div className="steps-container">
        {steps.map((step, index) => (
          <div className="step-card" key={index}>
            <div className="step-icon">{step.icon}</div>

            <h3>{step.title}</h3>

            <p>{step.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default HowItWorks;