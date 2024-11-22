import { Link } from "react-router-dom";
import "./HealthCheck.scss";

export const HealthCheck = () => {
  return (
    <div className="HealthCheck">
      <h2>Status: OK</h2>
      <p>You probably didn't mean to come here.</p>
      <Link to="/">Return to the homepage</Link>
    </div>
  );
};
