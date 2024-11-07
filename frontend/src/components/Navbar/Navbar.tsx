import { NavLink } from "react-router-dom";
import "./Navbar.scss";

export const Navbar = () => {
  return (
    <div className="Navbar">
      <h1 className="Navbar__title">Stephanie Bee Studio</h1>
      <div className="Navbar__links">
        <NavLink to="/">Available Artwork</NavLink>
        <NavLink to="/about">About</NavLink>
        <NavLink to="/gallery">Gallery</NavLink>
      </div>
    </div>
  );
};
