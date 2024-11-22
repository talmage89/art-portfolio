import * as React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import { Artwork, ArtworkModel } from '~/api';
import { Navbar } from '~/components';
import { useCartStore } from '~/data';
import '~/index.scss';
import './layout.scss';

export const Layout = () => {
  const initialLoadRef = React.useRef(true);
  const location = useLocation();

  const { cart, setCart } = useCartStore();

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
      <Navbar />
      <div className="Layout__content">
        <Outlet />
      </div>
      <ToastContainer />
    </div>
  );
};
