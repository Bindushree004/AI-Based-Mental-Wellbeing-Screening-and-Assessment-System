import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  updateProfile,
} from "firebase/auth";

import { auth } from "../firebase";


const API_BASE_URL = "http://localhost:5000/api";


// =========================================================
// REGISTER USER
// =========================================================

export const registerUser = async ({
  name,
  email,
  password,
}) => {

  try {

    // -----------------------------------------------------
    // Create account in Firebase Authentication
    // -----------------------------------------------------

    const userCredential =
      await createUserWithEmailAndPassword(
        auth,
        email,
        password
      );

    const user = userCredential.user;


    // -----------------------------------------------------
    // Store name in Firebase Authentication
    // -----------------------------------------------------

    await updateProfile(user, {
      displayName: name,
    });


    // -----------------------------------------------------
    // Get Firebase ID token
    // -----------------------------------------------------

    const token = await user.getIdToken();


    // -----------------------------------------------------
    // Create profile in Flask + Firestore
    // -----------------------------------------------------

    const response = await fetch(
      `${API_BASE_URL}/auth/register`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },

        body: JSON.stringify({
          name,
          email,
          phone: "",
        }),
      }
    );


    const data = await response.json();


    // -----------------------------------------------------
    // Check backend response
    // -----------------------------------------------------

    if (!response.ok) {

      throw new Error(
        data.message ||
        data.error ||
        "Failed to create user profile"
      );
    }


    console.log(
      "Registration response:",
      data
    );


    return data;

  } catch (error) {

    console.error(
      "Firebase registration error:",
      error
    );


    // -----------------------------------------------------
    // Firebase error handling
    // -----------------------------------------------------

    if (
      error.code ===
      "auth/email-already-in-use"
    ) {

      throw new Error(
        "An account with this email already exists."
      );
    }


    if (
      error.code ===
      "auth/invalid-email"
    ) {

      throw new Error(
        "Please enter a valid email address."
      );
    }


    if (
      error.code ===
      "auth/weak-password"
    ) {

      throw new Error(
        "Password must be at least 6 characters."
      );
    }


    if (
      error.code ===
      "auth/network-request-failed"
    ) {

      throw new Error(
        "Network error. Please check your connection."
      );
    }


    throw error;
  }
};


// =========================================================
// LOGIN USER
// =========================================================

export const loginUser = async ({
  email,
  password,
}) => {

  try {

    // -----------------------------------------------------
    // Login through Firebase Authentication
    // -----------------------------------------------------

    const userCredential =
      await signInWithEmailAndPassword(
        auth,
        email,
        password
      );

    const user = userCredential.user;


    // -----------------------------------------------------
    // Get Firebase ID token
    // -----------------------------------------------------

    const token =
      await user.getIdToken();


    // -----------------------------------------------------
    // Verify login through Flask backend
    // -----------------------------------------------------

    const response = await fetch(
      `${API_BASE_URL}/auth/login`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );


    const data = await response.json();


    // -----------------------------------------------------
    // Check backend response
    // -----------------------------------------------------

    if (!response.ok) {

      throw new Error(
        data.message ||
        data.error ||
        "Login verification failed"
      );
    }


    console.log(
      "Login response:",
      data
    );


    return data;

  } catch (error) {

    console.error(
      "Firebase login error:",
      error
    );


    // -----------------------------------------------------
    // Firebase login errors
    // -----------------------------------------------------

    if (
      error.code ===
        "auth/invalid-credential" ||
      error.code ===
        "auth/wrong-password" ||
      error.code ===
        "auth/user-not-found"
    ) {

      throw new Error(
        "Invalid email or password."
      );
    }


    if (
      error.code ===
      "auth/invalid-email"
    ) {

      throw new Error(
        "Please enter a valid email address."
      );
    }


    if (
      error.code ===
      "auth/user-disabled"
    ) {

      throw new Error(
        "This account has been disabled."
      );
    }


    if (
      error.code ===
      "auth/network-request-failed"
    ) {

      throw new Error(
        "Network error. Please check your connection."
      );
    }


    throw error;
  }
};


// =========================================================
// GET CURRENT LOGGED-IN USER
// =========================================================

export const getCurrentUser = async () => {

  try {

    // -----------------------------------------------------
    // Get currently logged-in Firebase user
    // -----------------------------------------------------

    const user = auth.currentUser;


    if (!user) {

      throw new Error(
        "No user is currently logged in."
      );
    }


    // -----------------------------------------------------
    // Get fresh Firebase ID token
    // -----------------------------------------------------

    const token =
      await user.getIdToken();


    // -----------------------------------------------------
    // Ask Flask backend for user profile
    // -----------------------------------------------------

    const response = await fetch(
      `${API_BASE_URL}/auth/me`,
      {
        method: "GET",

        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );


    const data = await response.json();


    // -----------------------------------------------------
    // Check backend response
    // -----------------------------------------------------

    if (!response.ok) {

      throw new Error(
        data.message ||
        data.error ||
        "Unable to retrieve user"
      );
    }


    console.log(
      "Current user:",
      data
    );


    return data;

  } catch (error) {

    console.error(
      "Get current user error:",
      error
    );

    throw error;
  }
};


// =========================================================
// LOGOUT
// =========================================================

export const logoutUser = async () => {

  try {

    await signOut(auth);

  } catch (error) {

    console.error(
      "Logout error:",
      error
    );

    throw error;
  }
};