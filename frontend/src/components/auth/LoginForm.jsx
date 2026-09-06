import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import {
  sendPasswordResetEmail,
} from "firebase/auth";

import {
  FaBrain,
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";

import { loginUser } from "../../api/auth";
import { auth } from "../../firebase";

import "../../styles/Login.css";

function LoginForm() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [loginSuccess, setLoginSuccess] = useState(false);
  const [loginFailed, setLoginFailed] = useState(false);

  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [resetEmail, setResetEmail] = useState("");
  const [resetLoading, setResetLoading] = useState(false);
  const [resetMessage, setResetMessage] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);

    try {
      const response = await loginUser({
        email: data.email.trim(),
        password: data.password,
      });

      console.log("Login response:", response);

      setLoginSuccess(true);

      setTimeout(() => {
        navigate("/dashboard");
      }, 3000);

    } catch (error) {
      console.error("Login error:", error);

      setLoginFailed(true);

      setTimeout(() => {
        setLoginFailed(false);
      }, 3000);

    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async (e) => {
    e.preventDefault();

    if (!resetEmail.trim()) {
      setResetMessage("Please enter your email address.");
      return;
    }

    setResetLoading(true);
    setResetMessage("");

    try {
      await sendPasswordResetEmail(
        auth,
        resetEmail.trim()
      );

      setResetMessage(
        "Password reset email sent successfully."
      );

    } catch (error) {
      console.error("Password reset error:", error);

      if (error.code === "auth/user-not-found") {
        setResetMessage(
          "No account found with this email."
        );
      } else if (error.code === "auth/invalid-email") {
        setResetMessage(
          "Please enter a valid email address."
        );
      } else {
        setResetMessage(
          "Unable to send reset email. Please try again."
        );
      }

    } finally {
      setResetLoading(false);
    }
  };

  return (
    <div className="login-container">

      {/* LOGIN CARD */}
      {!loginSuccess && !loginFailed && (
        <div className="login-card">

          {/* Logo */}
          <div className="login-logo">
            <FaBrain className="login-logo-icon" />
            <h2>MindSync AI</h2>
          </div>

          {/* Heading */}
          <h1>Welcome Back</h1>

          <p>
            Login to continue your mental wellbeing journey.
          </p>

          {/* Login Form */}
          <form onSubmit={handleSubmit(onSubmit)}>

            {/* Email */}
            <div className="input-group">
              <FaEnvelope className="input-icon" />

              <input
                type="email"
                placeholder="Email Address"
                {...register("email", {
                  required: "Email is required",
                  pattern: {
                    value: /^\S+@\S+\.\S+$/,
                    message: "Enter a valid email address",
                  },
                })}
              />
            </div>

            {errors.email && (
              <small>{errors.email.message}</small>
            )}

            {/* Password */}
            <div className="input-group">
              <FaLock className="input-icon" />

              <input
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                placeholder="Password"
                {...register("password", {
                  required: "Password is required",
                })}
              />

              <span
                className="eye-icon"
                onClick={() =>
                  setShowPassword(!showPassword)
                }
              >
                {showPassword ? (
                  <FaEyeSlash />
                ) : (
                  <FaEye />
                )}
              </span>
            </div>

            {errors.password && (
              <small>{errors.password.message}</small>
            )}

            {/* Forgot Password */}
            <div className="forgot-password">
              <button
                type="button"
                onClick={() => {
                  setShowForgotPassword(true);
                  setResetMessage("");
                }}
              >
                Forgot Password?
              </button>
            </div>

            {/* Login */}
            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Logging in..."
                : "Login"}
            </button>

          </form>

          {/* Signup */}
          <p className="signup-text">
            Don't have an account?

            <Link to="/signup">
              {" "}Sign Up
            </Link>
          </p>

        </div>
      )}

      {/* SUCCESS POPUP */}
      {loginSuccess && (
        <div className="login-success-popup">
          Login successful
        </div>
      )}

      {/* FAILED POPUP */}
      {loginFailed && (
        <div className="login-failed-popup">
          Login failed, try signing up
        </div>
      )}

      {/* FORGOT PASSWORD POPUP */}
      {showForgotPassword && (
        <div className="forgot-password-overlay">

          <div className="forgot-password-popup">

            <h2>Reset Password</h2>

            <p>
              Enter your email address and we'll
              send you a password reset link.
            </p>

            <form onSubmit={handleForgotPassword}>

              <div className="reset-input-group">
                <FaEnvelope />

                <input
                  type="email"
                  placeholder="Enter your email address"
                  value={resetEmail}
                  onChange={(e) =>
                    setResetEmail(e.target.value)
                  }
                  required
                />
              </div>

              <button
                type="submit"
                disabled={resetLoading}
              >
                {resetLoading
                  ? "Sending..."
                  : "Send Reset Email"}
              </button>

            </form>

            {resetMessage && (
              <p className="reset-message">
                {resetMessage}
              </p>
            )}

            <button
              className="close-reset"
              type="button"
              onClick={() => {
                setShowForgotPassword(false);
                setResetEmail("");
                setResetMessage("");
              }}
            >
              Cancel
            </button>

          </div>

        </div>
      )}

    </div>
  );
}

export default LoginForm;