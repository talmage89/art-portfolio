import * as React from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useCartStore, useTrackClick } from '~/data';
import './Navbar.scss';

type NavbarProps = {
  onCartOpen: () => void;
};

export const Navbar = ({ onCartOpen }: NavbarProps) => {
  const [menuOpen, setMenuOpen] = React.useState(false);

  const trackNavClick = useTrackClick('nav-link');

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
          <NavLink to="/" onClick={() => trackNavClick('Available Artwork')}>
            Available Artwork
          </NavLink>
          <NavLink to="/about" onClick={() => trackNavClick('About')}>
            About
          </NavLink>
          <NavLink to="/gallery" onClick={() => trackNavClick('Gallery')}>
            Gallery
          </NavLink>
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
  const { cart } = useCartStore();

  const trackNavClick = useTrackClick('nav-link');
  const trackCartClick = useTrackClick('cart');

  function handleLinkClick(name: string) {
    onClose();
    trackNavClick(name);
  }

  if (!isOpen) return null;

  return (
    <>
      <div className="Navbar__modal-overlay" onClick={onClose} />
      <div className="Navbar__modal">
        <div className="Navbar__modal__content">
          <NavLink to="/" onClick={() => handleLinkClick('Available Artwork')}>
            Available Artwork
          </NavLink>
          <NavLink to="/about" onClick={() => handleLinkClick('About')}>
            About
          </NavLink>
          <NavLink to="/gallery" onClick={() => handleLinkClick('Gallery')}>
            Gallery
          </NavLink>
          <button
            className="Navbar__modal__content__cart"
            onClick={() => {
              onClose();
              onCartOpen();
              trackCartClick('Mobile Cart Button');
            }}
          >
            My Cart - {cart.length} item{cart.length === 1 ? '' : 's'}
          </button>
        </div>
      </div>
    </>
  );
};
