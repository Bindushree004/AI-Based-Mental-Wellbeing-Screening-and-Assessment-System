import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

import {
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
  FaBrain,
} from "react-icons/fa";

import "../../styles/Login.css";

function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);

    console.log(data);

    // Simulating API call
    setTimeout(() => {
      toast.success("Login Successful!");

      setLoading(false);

      // Later we'll redirect to Dashboard here
      // navigate("/dashboard");

    }, 2000);
  };

  return (
    <div className="login-container">

      <div className="login-card">

        {/* Logo */}
        <div className="login-logo">
          <FaBrain className="login-logo-icon" />
          <h2>MindSync AI</h2>
        </div>

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
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </span>

          </div>

          {errors.password && (
            <small>{errors.password.message}</small>
          )}

          {/* Remember Me & Forgot Password */}
          <div className="login-options">

            <label>
              <input type="checkbox" />
              Remember Me
            </label>

            <Link to="/forgot-password">
              Forgot Password?
            </Link>

          </div>

          {/* Login Button */}
          <button type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>

        </form>

        {/* Signup Link */}
        <p className="signup-text">
          Don't have an account?
          <Link to="/signup"> Sign Up</Link>
        </p>

      </div>

    </div>
  );
}

export default LoginForm;