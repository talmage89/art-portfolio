import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '~/data';
import './CheckoutReturn.scss';

import checkIcon from '~/assets/check.png';

export const CheckoutReturn = () => {
  const navigate = useNavigate();

  const { setCart } = useCartStore();

  React.useEffect(() => {
    setCart([]);
  }, []);

  return (
    <div className="CheckoutReturn">
      <div className="CheckoutReturn__content">
        <img className="CheckoutReturn__icon" src={checkIcon} alt="Success" />
        <h1>Order Successful!</h1>
        <p>Your order has been received! A confirmation email will be sent to your email address.</p>
        <button className="CheckoutReturn__button" onClick={() => navigate('/')}>
          Continue shopping
        </button>
      </div>
    </div>
  );
};
