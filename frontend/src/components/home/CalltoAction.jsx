import { Link } from "react-router-dom";
import "../../styles/CallToAction.css";

function CallToAction() {
  return (
    <section className="cta">

      <h2>Ready to Start Your Mental Wellbeing Journey?</h2>

      <p>
        Take your first step towards better mental health with
        AI-powered screening, personalized insights, and
        wellbeing recommendations.
      </p>

      <Link to="/signup" className="cta-btn">
        Start Free Assessment
      </Link>

    </section>
  );
}

export default CallToAction;