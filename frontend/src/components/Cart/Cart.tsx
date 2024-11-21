import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShoppingCart, X } from 'lucide-react';
import { useCartStore } from '~/data';
import { Artwork, http } from '~/api';
import './Cart.scss';

interface CartProps {
  items: Artwork[];
  isOpen: boolean;
  onClose: () => void;
}

export const Cart = (props: CartProps) => {
  const [loading, setLoading] = React.useState(false);

  const navigate = useNavigate();
  const { removeFromCart } = useCartStore();

  function centsToDollars(cents: number) {
    return Number(cents / 100).toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
    });
  }

  function handleCheckout() {
    setLoading(true);
    http
      .post('/api/create-checkout-session/', { product_ids: props.items.map((item) => item.id) })
      .then((res) => (window.location.href = res.data.url))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }

  if (!props.isOpen) return null;

  return (
    <>
      <div className="Cart__overlay" onClick={props.onClose} />
      <div className="Cart">
        <div className="Cart__header">
          <span className="Cart__header__title">
            <ShoppingCart />
            <h2>Shopping Cart</h2>
          </span>
          <button className="Cart__close" onClick={props.onClose}>
            <X />
          </button>
        </div>
        <div className="Cart__content">
          {props.items.length === 0 ? (
            <p className="Cart__empty">Your cart is empty.</p>
          ) : (
            props.items.map((item) => (
              <div key={item.id} className="Cart__item">
                <img
                  src={item.images[0]?.image}
                  alt={item.title}
                  className="Cart__item__image"
                  onClick={() => {
                    props.onClose();
                    navigate(`/art/${item.id}`);
                  }}
                />
                <div className="Cart__item__details">
                  <h3
                    onClick={() => {
                      props.onClose();
                      navigate(`/art/${item.id}`);
                    }}
                  >
                    {item.title}
                  </h3>
                  <span className="Cart__item__details__info">
                    <p className="Cart__item__details__price">{centsToDollars(item.price_cents)}</p>
                    <a className="Cart__item__details__remove" onClick={() => removeFromCart(item.id)}>
                      Remove
                    </a>
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
        <div className="Cart__footer">
          <span className="Cart__footer__subtotal">
            <p className="Cart__footer__subtotal__label">Subtotal:</p>
            <p className="Cart__footer__subtotal__amount">
              {centsToDollars(props.items.reduce((acc, item) => acc + item.price_cents, 0))}
            </p>
          </span>
          <button
            className="Cart__footer__checkout"
            disabled={props.items.length === 0 || loading}
            onClick={handleCheckout}
          >
            {loading ? 'Loading...' : 'Secure Checkout'}
          </button>
        </div>
      </div>
    </>
  );
};
