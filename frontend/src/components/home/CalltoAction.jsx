import { useNavigate } from "react-router-dom";

function CallToAction() {
  const navigate = useNavigate();

  return (
    <section className="call-to-action">

      <h2>Take the First Step Towards Better Wellbeing</h2>

      <p>
        Understand your mental wellbeing and receive personalized
        recommendations through our assessment.
      </p>

      <button
        type="button"
        onClick={() => navigate("/assessment")}
      >
        Start Assessment
      </button>

    </section>
  );
}

export default CallToAction;