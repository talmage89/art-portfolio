import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '~/data';
import './CheckoutReturn.scss';

export const CheckoutReturn = () => {
  const navigate = useNavigate();

  const { setCart } = useCartStore();

  React.useEffect(() => {
    setCart([]);
  }, []);

  return (
    <div className="CheckoutReturn">
      <h2>Order Successful!</h2>
      <p>Your order has been received! A confirmation email will be sent to your email address.</p>
      <button className="CheckoutReturn__button" onClick={() => navigate('/')}>
        Continue shopping
      </button>
    </div>
  );
};
