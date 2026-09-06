import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "../pages/Home";
import About from "../pages/About";
import Login from "../pages/Login";
import Signup from "../pages/Signup";

import Dashboard from "../pages/Dashboard";
import Assessment from "../pages/Assessment";
import History from "../pages/History";
import Recommendations from "../pages/Recommendations";
import Profile from "../pages/Profile";

import DashboardLayout from "../components/DashboardLayout";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public pages */}
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Pages with Sidebar */}
        <Route element={<DashboardLayout />}>

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/assessment"
            element={<Assessment />}
          />

          <Route
            path="/history"
            element={<History />}
          />

          <Route
            path="/recommendations"
            element={<Recommendations />}
          />

          <Route
            path="/profile"
            element={<Profile />}
          />

        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;