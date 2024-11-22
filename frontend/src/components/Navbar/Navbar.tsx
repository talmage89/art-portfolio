import * as React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useCartStore } from '~/data';
import './Navbar.scss';

export const Navbar = () => {
  const [menuOpen, setMenuOpen] = React.useState(false);

  const { cart } = useCartStore();
  
  React.useEffect(() => {
    const mediaQuery = window.matchMedia('(min-width: 720px)');
    const handleResize = (e: MediaQueryListEvent) => {
      if (e.matches) {
        setMenuOpen(false);
      }
    };

    mediaQuery.addEventListener('change', handleResize);
    return () => mediaQuery.removeEventListener('change', handleResize);
  }, []);

  return (
    <div className="Navbar__container">
      <div className="Navbar">
        <h1 className="Navbar__title">Stephanie Bee Studio</h1>
        <div className="Navbar__links">
          <NavLink to="/">Available Artwork</NavLink>
          <NavLink to="/gallery">Gallery</NavLink>
          <NavLink to="/about">About</NavLink>
          <NavLink to="/cart">Cart{cart.length > 0 && ` (${cart.length})`}</NavLink>
        </div>
        <button className="Navbar__menu" onClick={() => setMenuOpen((p) => !p)}>
          {menuOpen ? <X /> : <Menu />}
        </button>
      </div>
      <MenuModal isOpen={menuOpen} onClose={() => setMenuOpen(false)} />
    </div>
  );
};

type MenuModalProps = {
  isOpen: boolean;
  onClose: () => void;
};

const MenuModal = ({ isOpen, onClose }: MenuModalProps) => {
  const { cart } = useCartStore();
  const navigate = useNavigate();

  if (!isOpen) return null;

  return (
    <>
      <div className="Navbar__modal-overlay" onClick={onClose} />
      <div className="Navbar__modal">
        <div className="Navbar__modal__content">
          <NavLink to="/" onClick={onClose}>
            Available Artwork
          </NavLink>
          <NavLink to="/gallery" onClick={onClose}>
            Gallery
          </NavLink>
          <NavLink to="/about" onClick={onClose}>
            About
          </NavLink>
          <button
            className="Navbar__modal__content__cart"
            onClick={() => {
              onClose();
              navigate('/cart');
            }}
          >
            My Cart - {cart.length} item{cart.length === 1 ? '' : 's'}
          </button>
        </div>
      </div>
    </>
  );
};
