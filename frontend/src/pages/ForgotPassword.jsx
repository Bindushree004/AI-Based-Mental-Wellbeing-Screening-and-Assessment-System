import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { FaBrain, FaEnvelope } from "react-icons/fa";
import { toast } from "react-toastify";

import "../styles/ForgotPassword.css";

function ForgotPassword() {
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);

    try {
      console.log("Forgot password request:", data);

      // Backend password-reset API will be connected here.

      toast.success(
        "If this email is registered, password reset instructions will be sent."
      );
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="forgot-container">

      <div className="forgot-card">

        <div className="forgot-logo">
          <FaBrain className="forgot-logo-icon" />
          <h2>MindSync AI</h2>
        </div>

        <h1>Forgot Password?</h1>

        <p>
          Enter your registered email address and we'll help you reset
          your password.
        </p>

        <form onSubmit={handleSubmit(onSubmit)}>

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

          <button type="submit" disabled={loading}>
            {loading ? "Sending..." : "Send Reset Link"}
          </button>

        </form>

        <p className="back-login">
          Remember your password?
          <Link to="/login"> Back to Login</Link>
        </p>

      </div>

    </div>
  );
}

export default ForgotPassword;