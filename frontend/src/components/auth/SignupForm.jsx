import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import {
  FaBrain,
  FaUser,
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";

import { registerUser } from "../../api/auth";

import "../../styles/Signup.css";

function SignupForm() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [signupSuccess, setSignupSuccess] = useState(false);
  const [signupFailed, setSignupFailed] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const password = watch("password");

  const onSubmit = async (data) => {
    setLoading(true);

    try {
      const response = await registerUser({
        name: data.name.trim(),
        email: data.email.trim(),
        password: data.password,
      });

      console.log("Registration response:", response);

      // Hide signup form and show success popup
      setSignupSuccess(true);

      // Go to login after 3 seconds
      setTimeout(() => {
        navigate("/login");
      }, 3000);

    } catch (error) {
      console.error("Signup error:", error);

      // Hide signup form and show failed popup
      setSignupFailed(true);

      // Hide failed popup after 3 seconds
      setTimeout(() => {
        setSignupFailed(false);
      }, 3000);

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">

      {/* Show signup form only when there is no success/failure popup */}
      {!signupSuccess && !signupFailed && (
        <div className="signup-card">

          {/* Logo */}
          <div className="signup-logo">
            <FaBrain className="signup-logo-icon" />
            <h2>MindSync AI</h2>
          </div>

          {/* Heading */}
          <h1>Create Account</h1>

          <p>
            Start your mental wellbeing journey with MindSync AI.
          </p>

          {/* Form */}
          <form onSubmit={handleSubmit(onSubmit)}>

            {/* Full Name */}
            <div className="input-group">
              <FaUser className="input-icon" />

              <input
                type="text"
                placeholder="Full Name"
                {...register("name", {
                  required: "Full name is required",
                  minLength: {
                    value: 2,
                    message: "Name must be at least 2 characters",
                  },
                })}
              />
            </div>

            {errors.name && (
              <small>{errors.name.message}</small>
            )}

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
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                {...register("password", {
                  required: "Password is required",
                  minLength: {
                    value: 6,
                    message: "Password must be at least 6 characters",
                  },
                })}
              />

              <span
                className="eye-icon"
                onClick={() =>
                  setShowPassword(!showPassword)
                }
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </span>
            </div>

            {errors.password && (
              <small>{errors.password.message}</small>
            )}

            {/* Confirm Password */}
            <div className="input-group">
              <FaLock className="input-icon" />

              <input
                type={
                  showConfirmPassword
                    ? "text"
                    : "password"
                }
                placeholder="Confirm Password"
                {...register("confirmPassword", {
                  required: "Please confirm your password",
                  validate: (value) =>
                    value === password ||
                    "Passwords do not match",
                })}
              />

              <span
                className="eye-icon"
                onClick={() =>
                  setShowConfirmPassword(
                    !showConfirmPassword
                  )
                }
              >
                {showConfirmPassword ? (
                  <FaEyeSlash />
                ) : (
                  <FaEye />
                )}
              </span>
            </div>

            {errors.confirmPassword && (
              <small>
                {errors.confirmPassword.message}
              </small>
            )}

            {/* Terms */}
            <label className="terms">

              <input
                type="checkbox"
                {...register("terms", {
                  required:
                    "You must accept the terms",
                })}
              />

              <span>
                I agree to the Terms & Conditions
              </span>

            </label>

            {errors.terms && (
              <small>{errors.terms.message}</small>
            )}

            {/* Create Account */}
            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Creating Account..."
                : "Create Account"}
            </button>

          </form>

          {/* Login */}
          <p className="login-text">
            Already have an account?

            <Link to="/login">
              {" "}Login
            </Link>
          </p>

        </div>
      )}

      {/* SUCCESS POPUP */}
      {signupSuccess && (
        <div className="signup-success-popup">
          SIGN UP SUCCESSFUL
        </div>
      )}

      {/* FAILED POPUP */}
      {signupFailed && (
        <div className="signup-failed-popup">
          SIGN UP FAILED
        </div>
      )}

    </div>
  );
}

export default SignupForm;