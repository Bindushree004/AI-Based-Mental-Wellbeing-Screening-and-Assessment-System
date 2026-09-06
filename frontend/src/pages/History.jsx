import { useEffect, useState } from "react";
import {
  FaClipboardCheck,
  FaCalendarAlt,
  FaArrowRight,
} from "react-icons/fa";
import { getIdToken } from "firebase/auth";

import { auth } from "../firebase";

import "./History.css";


function AssessmentHistory() {

  const [assessments, setAssessments] = useState([]);

  const [selectedAssessment, setSelectedAssessment] =
    useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  // =========================================================
  // FETCH ASSESSMENT HISTORY
  // =========================================================

  useEffect(() => {

    const fetchHistory = async () => {

      try {

        setLoading(true);
        setError("");

        // -------------------------------------------------
        // Get logged-in Firebase user
        // -------------------------------------------------

        const user = auth.currentUser;

        if (!user) {

          setError(
            "Please log in again to view your assessment history."
          );

          return;
        }

        // -------------------------------------------------
        // Get Firebase ID token
        // -------------------------------------------------

        const token = await getIdToken(
          user,
          true
        );

        // -------------------------------------------------
        // Call backend
        // -------------------------------------------------

        const response = await fetch(
          "http://localhost:5000/api/assessment/history",
          {
            method: "GET",

            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await response.json();

        // -------------------------------------------------
        // Check response
        // -------------------------------------------------

        if (!response.ok) {

          throw new Error(
            data.message ||
            "Failed to fetch assessment history."
          );
        }

        // -------------------------------------------------
        // Store assessments
        // -------------------------------------------------

        setAssessments(
          data.assessments || []
        );

      } catch (err) {

        console.error(
          "Assessment history error:",
          err
        );

        setError(
          err.message ||
          "Unable to load assessment history."
        );

      } finally {

        setLoading(false);

      }

    };


    fetchHistory();

  }, []);


  // =========================================================
  // RISK CLASS
  // =========================================================

  const getRiskClass = (riskLevel) => {

    if (!riskLevel) {
      return "";
    }

    return riskLevel
      .toString()
      .toLowerCase();

  };


  // =========================================================
  // LATEST ASSESSMENT
  // =========================================================

  const latestAssessment =
    assessments.length > 0
      ? assessments[0]
      : null;


  // =========================================================
  // LOADING
  // =========================================================

  if (loading) {

    return (

      <div className="history-page">

        <div className="history-header">

          <div className="history-title">

            <div className="history-icon">
              <FaClipboardCheck />
            </div>

            <div>

              <h1>
                Assessment History
              </h1>

              <p>
                View your previous mental wellbeing
                assessments and results.
              </p>

            </div>

          </div>

        </div>


        <div className="empty-history">

          <FaClipboardCheck />

          <h3>
            Loading assessment history...
          </h3>

        </div>

      </div>

    );

  }


  // =========================================================
  // ERROR
  // =========================================================

  if (error) {

    return (

      <div className="history-page">

        <div className="history-header">

          <div className="history-title">

            <div className="history-icon">
              <FaClipboardCheck />
            </div>

            <div>

              <h1>
                Assessment History
              </h1>

              <p>
                View your previous mental wellbeing
                assessments and results.
              </p>

            </div>

          </div>

        </div>


        <div className="empty-history">

          <FaClipboardCheck />

          <h3>
            Unable to load history
          </h3>

          <p>
            {error}
          </p>

        </div>

      </div>

    );

  }


  return (

    <div className="history-page">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="history-header">

        <div className="history-title">

          <div className="history-icon">
            <FaClipboardCheck />
          </div>

          <div>

            <h1>
              Assessment History
            </h1>

            <p>
              View your previous mental wellbeing
              assessments and results.
            </p>

          </div>

        </div>

      </div>


      {/* =====================================================
          SUMMARY
      ===================================================== */}

      <div className="history-summary">


        {/* Total */}

        <div className="summary-card">

          <div className="summary-number">

            {assessments.length}

          </div>

          <div>

            <span>
              Total Assessments
            </span>

            <p>
              Completed
            </p>

          </div>

        </div>


        {/* Latest Score */}

        <div className="summary-card">

          <div className="summary-number">

            {latestAssessment?.wellbeingScore ??
              "--"}

          </div>

          <div>

            <span>
              Latest Score
            </span>

            <p>
              Out of 100
            </p>

          </div>

        </div>


        {/* Latest Risk */}

        <div className="summary-card">

          <div
            className={`summary-risk ${
              getRiskClass(
                latestAssessment?.riskLevel
              )
            }`}
          >

            {latestAssessment?.riskLevel ??
              "--"}

          </div>

          <div>

            <span>
              Latest Risk Level
            </span>

            <p>
              Current assessment
            </p>

          </div>

        </div>


      </div>


      {/* =====================================================
          HISTORY SECTION
      ===================================================== */}

      <div className="history-section">


        <div className="section-header">

          <h2>
            Previous Assessments
          </h2>

          <span>

            {assessments.length}{" "}
            {assessments.length === 1
              ? "assessment"
              : "assessments"}

          </span>

        </div>


        <div className="history-list">


          {assessments.length === 0 ? (

            <div className="empty-history">

              <FaClipboardCheck />

              <h3>
                No assessments yet
              </h3>

              <p>
                Complete your first mental wellbeing
                assessment to see your results here.
              </p>

            </div>

          ) : (

            assessments.map(
              (assessment) => (

                <div
                  className="history-card"
                  key={assessment.id}
                >


                  {/* =========================================
                      LEFT
                  ========================================= */}

                  <div className="history-card-left">

                    <div className="assessment-number">

                      <FaClipboardCheck />

                    </div>


                    <div className="assessment-info">

                      <h3>

                        Assessment #
                        {assessment.assessmentNumber}

                      </h3>


                      <div className="assessment-date">

                        <FaCalendarAlt />

                        <span>

                          {assessment.createdAt ||
                            "Unknown date"}

                        </span>

                      </div>

                    </div>

                  </div>


                  {/* =========================================
                      SCORE
                  ========================================= */}

                  <div className="history-score">

                    <span>
                      Score
                    </span>

                    <strong>

                      {assessment.wellbeingScore ??
                        "--"}

                      <small>
                        /100
                      </small>

                    </strong>

                  </div>


                  {/* =========================================
                      RISK
                  ========================================= */}

                  <div className="history-risk">

                    <span>
                      Risk Level
                    </span>


                    <div
                      className={`risk-badge ${
                        getRiskClass(
                          assessment.riskLevel
                        )
                      }`}
                    >

                      {assessment.riskLevel ??
                        "--"}

                    </div>

                  </div>


                  {/* =========================================
                      STATUS
                  ========================================= */}

                  <div className="history-status">

                    <span className="status-badge">

                      {assessment.status ||
                        "Completed"}

                    </span>

                  </div>


                  {/* =========================================
                      VIEW
                  ========================================= */}

                  <button
                    type="button"
                    className="view-result-button"
                    onClick={() =>
                      setSelectedAssessment(
                        assessment
                      )
                    }
                  >

                    View

                    <FaArrowRight />

                  </button>


                </div>

              )
            )

          )}

        </div>

      </div>


      {/* =====================================================
          RESULT MODAL
      ===================================================== */}

      {selectedAssessment && (

        <div
          className="result-overlay"
          onClick={() =>
            setSelectedAssessment(null)
          }
        >


          <div
            className="result-modal"
            onClick={(e) =>
              e.stopPropagation()
            }
          >


            {/* Close */}

            <button
              type="button"
              className="close-modal"
              onClick={() =>
                setSelectedAssessment(null)
              }
            >

              ×

            </button>


            {/* Title */}

            <h2>

              Assessment #
              {selectedAssessment.assessmentNumber}

            </h2>


            <p className="modal-date">

              Completed on{" "}

              {selectedAssessment.createdAt ||
                "Unknown date"}

            </p>


            {/* =============================================
                SCORE
            ============================================= */}

            <div className="modal-score">

              <span>
                Overall Wellbeing Score
              </span>

              <strong>

                {selectedAssessment.wellbeingScore ??
                  "--"}

                <small>
                  /100
                </small>

              </strong>

            </div>


            {/* =============================================
                RISK
            ============================================= */}

            <div className="modal-risk">

              <span>
                Risk Level
              </span>


              <div
                className={`risk-badge large ${
                  getRiskClass(
                    selectedAssessment.riskLevel
                  )
                }`}
              >

                {selectedAssessment.riskLevel ??
                  "--"}

              </div>

            </div>


            {/* =============================================
                ANALYSIS
            ============================================= */}

            <div className="modal-section">

              <h3>
                AI Analysis
              </h3>


              <p>

                {selectedAssessment.analysis ||
                  "No analysis is available for this assessment."}

              </p>

            </div>


            {/* =============================================
                RECOMMENDATIONS
            ============================================= */}

            <div className="modal-section">

              <h3>
                Recommendations
              </h3>


              {Array.isArray(
                selectedAssessment.recommendations
              ) &&
              selectedAssessment.recommendations.length >
                0 ? (

                <ul>

                  {selectedAssessment.recommendations.map(
                    (recommendation, index) => (

                      <li key={index}>

                        {recommendation}

                      </li>

                    )
                  )}

                </ul>

              ) : (

                <p>
                  No recommendations are available
                  for this assessment.
                </p>

              )}

            </div>


          </div>

        </div>

      )}

    </div>

  );

}


export default AssessmentHistory;