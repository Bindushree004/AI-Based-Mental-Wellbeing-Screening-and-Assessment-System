import { useEffect, useState } from "react";

import {
  FaLightbulb,
  FaBrain,
  FaBed,
  FaDumbbell,
  FaMobileAlt,
  FaUsers,
  FaHeart,
  FaArrowRight,
} from "react-icons/fa";

import "./Recommendations.css";


function Recommendations() {

  const [recommendations, setRecommendations] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [hasAssessment, setHasAssessment] = useState(false);


  // =====================================================
  // GET FIREBASE TOKEN
  // =====================================================

  const getToken = async () => {

    const { getAuth } = await import("firebase/auth");

    const auth = getAuth();

    const user = auth.currentUser;

    if (!user) {
      throw new Error("User is not logged in");
    }

    return await user.getIdToken();
  };


  // =====================================================
  // FETCH RECOMMENDATIONS
  // =====================================================

  useEffect(() => {

    const fetchRecommendations = async () => {

      try {

        setLoading(true);

        setError("");

        const token = await getToken();

        const response = await fetch(
          "http://127.0.0.1:5000/api/recommendations",
          {
            method: "GET",

            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );


        const data = await response.json();


        if (!response.ok) {

          throw new Error(
            data.message ||
            "Failed to fetch recommendations"
          );

        }


        setRecommendations(
          data.recommendations || []
        );


        setHasAssessment(
          data.hasAssessment || false
        );


      } catch (err) {

        console.error(
          "Recommendation error:",
          err
        );

        setError(
          err.message ||
          "Unable to load recommendations"
        );

      } finally {

        setLoading(false);

      }

    };


    fetchRecommendations();

  }, []);


  // =====================================================
  // ICON
  // =====================================================

  const getIcon = (icon) => {

    switch (icon) {

      case "sleep":
        return <FaBed />;

      case "activity":
        return <FaDumbbell />;

      case "screen":
        return <FaMobileAlt />;

      case "social":
        return <FaUsers />;

      case "support":
        return <FaHeart />;

      case "stress":
        return <FaBrain />;

      case "anxiety":
        return <FaBrain />;

      case "mood":
        return <FaHeart />;

      case "focus":
        return <FaBrain />;

      default:
        return <FaLightbulb />;

    }

  };


  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {

    return (

      <div className="recommendations-page">

        <div className="recommendations-loading">

          <FaLightbulb />

          <h2>
            Generating Recommendations...
          </h2>

          <p>
            Analyzing your latest wellbeing assessment.
          </p>

        </div>

      </div>

    );

  }


  // =====================================================
  // ERROR
  // =====================================================

  if (error) {

    return (

      <div className="recommendations-page">

        <div className="recommendations-error">

          <FaLightbulb />

          <h2>
            Unable to Load Recommendations
          </h2>

          <p>
            {error}
          </p>

        </div>

      </div>

    );

  }


  // =====================================================
  // PAGE
  // =====================================================

  return (

    <div className="recommendations-page">


      {/* ================================================
          HEADER
      ================================================= */}

      <div className="recommendations-header">

        <div className="recommendations-title">

          <div className="recommendations-icon">

            <FaLightbulb />

          </div>


          <div>

            <h1>
              Recommendations
            </h1>

            <p>
              Personalized suggestions to support your
              mental wellbeing.
            </p>

          </div>

        </div>

      </div>


      {/* ================================================
          INTRODUCTION
      ================================================= */}

      <div className="recommendations-intro">

        <div className="intro-icon">

          <FaBrain />

        </div>


        <div>

          <h2>
            Your Wellbeing Recommendations
          </h2>

          <p>

            {hasAssessment

              ? "Based on your latest assessment responses, here are some areas that may help support your mental wellbeing."

              : "Complete an assessment to receive personalized wellbeing recommendations."

            }

          </p>

        </div>

      </div>


      {/* ================================================
          RECOMMENDATIONS
      ================================================= */}

      {recommendations.length > 0 ? (

        <div className="suggestions-section">


          <div className="suggestions-header">

            <h2>
              Suggestions for You
            </h2>

            <span>
              {recommendations.length} recommendations
            </span>

          </div>


          <div className="recommendations-grid">


            {recommendations.map(
              (recommendation, index) => (

                <div
                  className="recommendation-card"
                  key={`${recommendation.title}-${index}`}
                >


                  {/* Icon */}

                  <div className="recommendation-top">

                    <div className="recommendation-card-icon">

                      {getIcon(
                        recommendation.icon
                      )}

                    </div>


                    <span className="recommendation-category">

                      {recommendation.category}

                    </span>

                  </div>


                  {/* Title */}

                  <h3>
                    {recommendation.title}
                  </h3>


                  {/* Description */}

                  <p>
                    {recommendation.description}
                  </p>


                  {/* Footer */}

                  <div className="recommendation-footer">

                    <span>
                      Wellbeing Tip
                    </span>

                    <FaArrowRight />

                  </div>


                </div>

              )
            )}

          </div>

        </div>

      ) : (

        <div className="no-recommendations">

          <FaLightbulb />

          <h2>
            No Recommendations Yet
          </h2>

          <p>
            Complete a mental wellbeing assessment
            to receive personalized suggestions.
          </p>

        </div>

      )}


      {/* ================================================
          DISCLAIMER
      ================================================= */}

      <div className="recommendations-disclaimer">

        <FaLightbulb />

        <p>

          These recommendations are intended for general
          wellbeing and awareness purposes. They are not a
          substitute for professional medical advice.

        </p>

      </div>


    </div>

  );

}


export default Recommendations;