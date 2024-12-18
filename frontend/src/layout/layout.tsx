import * as React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { ShoppingCart } from 'lucide-react';
import { Artwork, ArtworkModel } from '~/api';
import { Cart, Navbar } from '~/components';
import { useCartStore, useTrackClick } from '~/data';
import '~/index.scss';
import './layout.scss';

export const Layout = () => {
  const [cartOpen, setCartOpen] = React.useState(false);
  const initialLoadRef = React.useRef(true);
  const location = useLocation();

  const { cart, setCart } = useCartStore();
  const trackCartClick = useTrackClick('cart');

  React.useEffect(() => {
    if (initialLoadRef.current) {
      const cartJSON = localStorage.getItem('cart');
      const cart = cartJSON ? JSON.parse(cartJSON) : [];

      Promise.allSettled(cart.map((item: Artwork) => ArtworkModel.get(item.id).then((artwork) => artwork.data))).then(
        (artworks) => {
          const filteredArtworks = artworks
            .filter(
              (promise): promise is PromiseFulfilledResult<Artwork> =>
                promise.status === 'fulfilled' && promise.value.status === 'available'
            )
            .map((promise) => promise.value);
          setCart(filteredArtworks);
        }
      );

      initialLoadRef.current = false;
    } else {
      localStorage.setItem('cart', JSON.stringify(cart));
    }
  }, [cart]);

  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, [location]);

  return (
    <div className="Layout">
      <Navbar onCartOpen={() => setCartOpen(true)} />
      <div
        className="Layout__cartBadge"
        onClick={() => {
          setCartOpen(true);
          trackCartClick('Cart Badge');
        }}
      >
        <div className="Layout__cartBadge__data">
          <ShoppingCart className="Layout__cartBadge__data__icon" />
          <p className="Layout__cartBadge__data__count">{cart.length}</p>
        </div>
      </div>
      <div className="Layout__content">
        <Outlet />
      </div>
      {/* <Footer /> */}
      <Cart items={cart} isOpen={cartOpen} onClose={() => setCartOpen(false)} />
    </div>
  );
};
