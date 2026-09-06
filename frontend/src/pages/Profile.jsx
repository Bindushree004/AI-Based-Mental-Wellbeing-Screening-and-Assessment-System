import { useEffect, useState } from "react";
import {
  FaUser,
  FaEnvelope,
  FaPhone,
  FaEdit,
  FaSave,
  FaTimes,
  FaSignOutAlt,
} from "react-icons/fa";

import {
  getAuth,
  updateProfile,
  signOut,
  onAuthStateChanged,
} from "firebase/auth";

import { useNavigate } from "react-router-dom";

import "./Profile.css";

function Profile() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  const [isEditing, setIsEditing] = useState(false);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // =========================================
  // GET CURRENT FIREBASE USER
  // =========================================

  useEffect(() => {
    const auth = getAuth();

    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        navigate("/login");
        return;
      }

      try {
        // Make sure the latest Firebase profile data is loaded
        await currentUser.reload();

        const updatedUser = auth.currentUser;

        setUser(updatedUser);

        setName(updatedUser.displayName || "");
        setEmail(updatedUser.email || "");
        setPhone(updatedUser.phoneNumber || "");

      } catch (err) {
        console.error("Profile loading error:", err);

        setError("Unable to load profile information.");
      } finally {
        setLoading(false);
      }
    });

    return () => unsubscribe();
  }, [navigate]);

  // =========================================
  // SAVE PROFILE
  // =========================================

  const handleSave = async () => {
    try {
      setSaving(true);
      setError("");
      setSuccess("");

      const auth = getAuth();

      const currentUser = auth.currentUser;

      if (!currentUser) {
        throw new Error("User is not logged in.");
      }

      const trimmedName = name.trim();

      if (!trimmedName) {
        throw new Error("Please enter your full name.");
      }

      // Update Firebase Authentication profile
      await updateProfile(currentUser, {
        displayName: trimmedName,
      });

      // Reload Firebase user so currentUser contains latest data
      await currentUser.reload();

      const updatedUser = auth.currentUser;

      // Update local state
      setUser(updatedUser);
      setName(updatedUser.displayName || "");

      setIsEditing(false);

      setSuccess("Profile updated successfully.");

      // Tell other components/pages that profile changed
      window.dispatchEvent(
        new CustomEvent("profileUpdated", {
          detail: {
            displayName: updatedUser.displayName || "",
          },
        })
      );

    } catch (err) {
      console.error("Profile update error:", err);

      setError(
        err.message || "Unable to update profile."
      );

    } finally {
      setSaving(false);
    }
  };

  // =========================================
  // CANCEL EDIT
  // =========================================

  const handleCancel = () => {
    setName(user?.displayName || "");

    setIsEditing(false);

    setError("");
    setSuccess("");
  };

  // =========================================
  // LOGOUT
  // =========================================

  const handleLogout = async () => {
    try {
      const auth = getAuth();

      await signOut(auth);

      navigate("/login");

    } catch (err) {
      console.error("Logout error:", err);

      setError("Unable to logout. Please try again.");
    }
  };

  // =========================================
  // LOADING
  // =========================================

  if (loading) {
    return (
      <div className="profile-page">

        <div className="profile-loading">

          <FaUser />

          <h2>Loading Profile...</h2>

          <p>
            Please wait while we load your profile information.
          </p>

        </div>

      </div>
    );
  }

  // =========================================
  // PROFILE
  // =========================================

  return (
    <div className="profile-page">

      {/* =====================================
          HEADER
      ===================================== */}

      <div className="profile-header">

        <div className="profile-title">

          <div className="profile-title-icon">
            <FaUser />
          </div>

          <div>

            <h1>My Profile</h1>

            <p>
              Manage your account information and profile details.
            </p>

          </div>

        </div>

      </div>


      {/* =====================================
          PROFILE CONTAINER
      ===================================== */}

      <div className="profile-container">

        {/* ===================================
            PROFILE CARD
        =================================== */}

        <div className="profile-card">

          {/* PROFILE HEADER */}

          <div className="profile-card-header">

            <div className="profile-avatar">
              <FaUser />
            </div>

            <div className="profile-user-info">

              <h2>
                {user?.displayName || "User"}
              </h2>

              <p>
                {user?.email || "No email available"}
              </p>

            </div>

          </div>


          {/* MESSAGES */}

          {success && (
            <div className="profile-success">
              {success}
            </div>
          )}

          {error && (
            <div className="profile-error">
              {error}
            </div>
          )}


          {/* PROFILE DETAILS */}

          <div className="profile-details">

            {/* NAME */}

            <div className="profile-field">

              <label>
                Full Name
              </label>

              <div className="profile-input-wrapper">

                <FaUser />

                <input
                  type="text"
                  value={name}
                  onChange={(e) =>
                    setName(e.target.value)
                  }
                  disabled={!isEditing}
                  placeholder="Enter your full name"
                />

              </div>

            </div>


            {/* EMAIL */}

            <div className="profile-field">

              <label>
                Email Address
              </label>

              <div className="profile-input-wrapper">

                <FaEnvelope />

                <input
                  type="email"
                  value={email}
                  disabled
                />

              </div>

              <small>
                Email address is managed by your account.
              </small>

            </div>


            {/* PHONE */}

            <div className="profile-field">

              <label>
                Phone Number
              </label>

              <div className="profile-input-wrapper">

                <FaPhone />

                <input
                  type="text"
                  value={phone || "Not provided"}
                  disabled
                />

              </div>

            </div>

          </div>


          {/* ACTIONS */}

          <div className="profile-actions">

            {!isEditing ? (

              <button
                type="button"
                className="edit-profile-button"
                onClick={() => {
                  setIsEditing(true);
                  setSuccess("");
                  setError("");
                }}
              >
                <FaEdit />
                Edit Profile
              </button>

            ) : (

              <div className="editing-actions">

                <button
                  type="button"
                  className="save-profile-button"
                  onClick={handleSave}
                  disabled={saving}
                >
                  <FaSave />

                  {saving
                    ? "Saving..."
                    : "Save Changes"}
                </button>

                <button
                  type="button"
                  className="cancel-profile-button"
                  onClick={handleCancel}
                  disabled={saving}
                >
                  <FaTimes />
                  Cancel
                </button>

              </div>

            )}

          </div>

        </div>


        {/* =====================================
            ACCOUNT CARD
        ===================================== */}

        <div className="account-card">

          <div className="account-card-header">

            <div>

              <h2>Account</h2>

              <p>
                Manage your MindSync AI account.
              </p>

            </div>

          </div>

          <button
            type="button"
            className="logout-button"
            onClick={handleLogout}
          >
            <FaSignOutAlt />
            Logout
          </button>

        </div>

      </div>

    </div>
  );
}

export default Profile;