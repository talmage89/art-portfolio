import * as React from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useCartStore } from '~/data';
import './Navbar.scss';

type NavbarProps = {
  onCartOpen: () => void;
};

export const Navbar = ({ onCartOpen }: NavbarProps) => {
  const [menuOpen, setMenuOpen] = React.useState(false);

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
          <NavLink to="/about">About</NavLink>
          <NavLink to="/gallery">Gallery</NavLink>
        </div>
        <button className="Navbar__menu" onClick={() => setMenuOpen((p) => !p)}>
          {menuOpen ? <X /> : <Menu />}
        </button>
      </div>
      <MenuModal isOpen={menuOpen} onClose={() => setMenuOpen(false)} onCartOpen={onCartOpen} />
    </div>
  );
};

type MenuModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onCartOpen: () => void;
};

const MenuModal = ({ isOpen, onClose, onCartOpen }: MenuModalProps) => {
  if (!isOpen) return null;

  const { cart } = useCartStore();

  return (
    <>
      <div className="Navbar__modal-overlay" onClick={onClose} />
      <div className="Navbar__modal">
        <div className="Navbar__modal__content">
          <NavLink to="/" onClick={onClose}>
            Available Artwork
          </NavLink>
          <NavLink to="/about" onClick={onClose}>
            About
          </NavLink>
          <NavLink to="/gallery" onClick={onClose}>
            Gallery
          </NavLink>
          <button
            className="Navbar__modal__content__cart"
            onClick={() => {
              onClose();
              onCartOpen();
            }}
          >
            My Cart - {cart.length} item{cart.length === 1 ? '' : 's'}
          </button>
        </div>
      </div>
    </>
  );
};
