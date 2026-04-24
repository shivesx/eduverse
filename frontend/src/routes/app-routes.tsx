import { Routes, Route } from "react-router-dom";
import Landing from "../pages/landing";
import Login from "../pages/auth/login";

import StudentRoutes from "./student-routes";
import CollegeRoutes from "./college-routes";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />

      <Route path="/student/*" element={<StudentRoutes />} />
      <Route path="/college/*" element={<CollegeRoutes />} />
    </Routes>
  );
};

export default AppRoutes;
