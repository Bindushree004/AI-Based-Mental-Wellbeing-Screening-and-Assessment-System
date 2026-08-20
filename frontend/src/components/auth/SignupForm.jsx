import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

import {
  FaBrain,
  FaUser,
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";

import "../../styles/Signup.css";

function SignupForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const password = watch("password");

  const onSubmit = (data) => {
    setLoading(true);

    console.log(data);

    setTimeout(() => {
      toast.success("Account Created Successfully!");
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="signup-container">
      <div className="signup-card">

        <div className="signup-logo">
          <FaBrain className="signup-logo-icon" />
          <h2>MindSync AI</h2>
        </div>

        <form onSubmit={handleSubmit(onSubmit)}>

          {/* Full Name */}

          <div className="input-group">
            <FaUser className="input-icon" />

            <input
              type="text"
              placeholder="Full Name"
              {...register("name", {
                required: "Full Name is required",
              })}
            />
          </div>

          {errors.name && <small>{errors.name.message}</small>}

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
                  message: "Enter a valid email",
                },
              })}
            />
          </div>

          {errors.email && <small>{errors.email.message}</small>}

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
                  message: "Minimum 6 characters",
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

          {errors.password && <small>{errors.password.message}</small>}

          {/* Confirm Password */}

          <div className="input-group">
            <FaLock className="input-icon" />

            <input
              type={showConfirm ? "text" : "password"}
              placeholder="Confirm Password"
              {...register("confirmPassword", {
                required: "Confirm your password",
                validate: (value) =>
                  value === password || "Passwords do not match",
              })}
            />

            <span
              className="eye-icon"
              onClick={() => setShowConfirm(!showConfirm)}
            >
              {showConfirm ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>

          {errors.confirmPassword && (
            <small>{errors.confirmPassword.message}</small>
          )}

          {/* Terms */}

          <label className="terms">
            <input
              type="checkbox"
              {...register("terms", {
                required: "Accept Terms & Conditions",
              })}
            />

            I agree to the Terms & Conditions
          </label>

          {errors.terms && <small>{errors.terms.message}</small>}

          <button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Create Account"}
          </button>

        </form>

        <p className="login-text">
          Already have an account?
          <Link to="/login"> Login</Link>
        </p>

      </div>
    </div>
  );
}

export default SignupForm;