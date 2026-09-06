import { useEffect, useState } from "react";
import { onAuthStateChanged } from "firebase/auth";

import Sidebar from "../components/layout/Sidebar";
import { auth } from "../firebase";

import "./Dashboard.css";

const API_BASE_URL = "http://localhost:5000/api";

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (!user) {
        setError("User is not logged in.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError("");

        // Get Firebase ID token
        const token = await user.getIdToken();

        // Fetch dashboard data from Flask backend
        const response = await fetch(
          `${API_BASE_URL}/dashboard`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        const data = await response.json();

        console.log("Dashboard response:", data);

        if (!response.ok) {
          throw new Error(
            data.message || "Failed to load dashboard"
          );
        }

        setDashboardData(data);

      } catch (err) {
        console.error("Dashboard error:", err);
        setError(err.message || "Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    });

    return () => unsubscribe();
  }, []);

  // Loading
  if (loading) {
    return (
      <div className="dashboard-page">
        <Sidebar />

        <main className="dashboard-content">
          <div className="dashboard-loading">
            Loading dashboard...
          </div>
        </main>
      </div>
    );
  }

  // Error
  if (error) {
    return (
      <div className="dashboard-page">
        <Sidebar />

        <main className="dashboard-content">
          <div className="dashboard-error">
            {error}
          </div>
        </main>
      </div>
    );
  }

  const dashboard = dashboardData?.dashboard || {};
  const latestAssessment =
    dashboardData?.latestAssessment || null;

  const user = dashboardData?.user || {};

  // Format date
  const formatDate = (dateValue) => {
    if (!dateValue) {
      return "--";
    }

    try {
      let date;

      // Firestore timestamp returned as object
      if (
        typeof dateValue === "object" &&
        dateValue._seconds
      ) {
        date = new Date(dateValue._seconds * 1000);
      }

      // Firestore timestamp returned with seconds
      else if (
        typeof dateValue === "object" &&
        dateValue.seconds
      ) {
        date = new Date(dateValue.seconds * 1000);
      }

      // Normal date/string
      else {
        date = new Date(dateValue);
      }

      if (isNaN(date.getTime())) {
        return "--";
      }

      return date.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      });

    } catch {
      return "--";
    }
  };

  return (
    <div className="dashboard-page">

      {/* Sidebar */}
      <Sidebar />

      {/* Dashboard Main Content */}
      <main className="dashboard-content">

        {/* Header */}
        <div className="dashboard-header">

          <h1>
            Welcome to{" "}
            {user.name
              ? `${user.name}`
              : "MindSync AI"}
          </h1>

          <p>
            Here's an overview of your mental wellbeing.
          </p>

        </div>

        {/* Stats */}
        <div className="dashboard-stats">

          {/* Wellbeing Score */}
          <div className="stat-card">

            <h3>Wellbeing Score</h3>

            <p className="stat-value">
              {dashboard.wellbeingScore !== null &&
              dashboard.wellbeingScore !== undefined
                ? `${dashboard.wellbeingScore} / 100`
                : "-- / 100"}
            </p>

            <span>
              {dashboard.wellbeingScore !== null &&
              dashboard.wellbeingScore !== undefined
                ? "Latest assessment score"
                : "Complete an assessment"}
            </span>

          </div>

          {/* Risk Level */}
          <div className="stat-card">

            <h3>Risk Level</h3>

            <p className="stat-value">
              {dashboard.riskLevel || "--"}
            </p>

            <span>
              {dashboard.riskLevel
                ? "Based on latest assessment"
                : "Assessment required"}
            </span>

          </div>

          {/* Assessments Completed */}
          <div className="stat-card">

            <h3>Assessments Completed</h3>

            <p className="stat-value">
              {dashboard.assessmentsCompleted ?? 0}
            </p>

            <span>
              Total assessments
            </span>

          </div>

          {/* Last Assessment */}
          <div className="stat-card">

            <h3>Last Assessment</h3>

            <p className="stat-value">
              {formatDate(dashboard.lastAssessment)}
            </p>

            <span>
              {dashboard.lastAssessment
                ? "Most recent assessment"
                : "No assessment yet"}
            </span>

          </div>

        </div>

        {/* Latest Assessment Result */}
        <section className="dashboard-card">

          <div className="card-header">

            <div>

              <h2>
                Latest Assessment Result
              </h2>

              <p>
                Your most recent wellbeing assessment
                will appear here.
              </p>

            </div>

          </div>

          {latestAssessment ? (

            <div className="latest-result">

              <div className="result-score">

                <span>
                  {latestAssessment.wellbeingScore ?? "--"}
                </span>

                <small>
                  / 100
                </small>

              </div>

              <div className="result-info">

                <h3>
                  {latestAssessment.riskLevel
                    ? `Risk Level: ${latestAssessment.riskLevel}`
                    : "Assessment Completed"}
                </h3>

                <p>
                  Assessment completed on{" "}
                  {formatDate(
                    latestAssessment.createdAt
                  )}
                </p>

              </div>

            </div>

          ) : (

            <div className="latest-result">

              <div className="result-score">

                <span>
                  --
                </span>

                <small>
                  / 100
                </small>

              </div>

              <div className="result-info">

                <h3>
                  No Assessment Available
                </h3>

                <p>
                  Complete your first wellbeing
                  assessment to receive your
                  personalized result.
                </p>

              </div>

            </div>

          )}

        </section>

        {/* AI Recommendations */}
        <section className="dashboard-card">

          <div className="card-header">

            <div>

              <h2>
                AI Recommendations
              </h2>

              <p>
                Personalized recommendations based
                on your wellbeing assessment.
              </p>

            </div>

          </div>

          {latestAssessment?.recommendation ? (

            <div className="recommendation-empty">

              <p>
                {latestAssessment.recommendation}
              </p>

            </div>

          ) : (

            <div className="recommendation-empty">

              <p>
                Complete an assessment to receive
                personalized recommendations.
              </p>

            </div>

          )}

        </section>

        {/* Quick Actions */}
        <section className="quick-actions">

          <h2>
            Quick Actions
          </h2>

          <div className="action-buttons">

            <button
              type="button"
              onClick={() => {
                window.location.href = "/assessment";
              }}
            >
              Take Assessment
            </button>

            <button
              type="button"
              onClick={() => {
                window.location.href = "/history";
              }}
            >
              View Assessment History
            </button>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;