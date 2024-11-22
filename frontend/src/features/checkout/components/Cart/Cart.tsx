import { useNavigate } from 'react-router-dom';
import { useCartStore } from '~/data';
import { CheckoutFooter } from '..';
import './Cart.scss';

type CartProps = {
  onProceed: () => void;
};

export const Cart = (props: CartProps) => {
  const navigate = useNavigate();
  const { cart, removeFromCart } = useCartStore();

  function centsToDollars(cents: number) {
    return Number(cents / 100).toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
    });
  }

  return (
    <div className="Cart">
      <div className="Cart__content">
        {cart.length === 0 ? (
          <p className="Cart__empty">Your cart is empty.</p>
        ) : (
          cart.map((item) => (
            <div key={item.id} className="Cart__item">
              <img
                src={item.images[0]?.image}
                alt={item.title}
                className="Cart__item__image"
                onClick={() => {
                  navigate(`/art/${item.id}`);
                }}
              />
              <div className="Cart__item__details">
                <h3
                  onClick={() => {
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
      <CheckoutFooter
        text="Proceed to Checkout"
        onClick={props.onProceed}
        disabled={cart.length === 0}
      />
    </div>
  );
};
