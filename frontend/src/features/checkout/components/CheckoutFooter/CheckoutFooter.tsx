import { useCartStore } from '~/data';
import './CheckoutFooter.scss';

type CheckoutFooterProps = {
  text: string;
  onClick: () => void;
  loading?: boolean;
  disabled?: boolean;
};

export const CheckoutFooter = (props: CheckoutFooterProps) => {
  const { cart } = useCartStore();

  function centsToDollars(cents: number) {
    return Number(cents / 100).toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
    });
  }

  return (
    <div className="CheckoutFooter">
      <span className="CheckoutFooter__subtotal">
        <p className="CheckoutFooter__subtotal__label">Subtotal:</p>
        <p className="CheckoutFooter__subtotal__amount">
          {centsToDollars(cart.reduce((acc, item) => acc + item.price_cents, 0))}
        </p>
      </span>
      <button className="CheckoutFooter__checkout" disabled={props.disabled} onClick={props.onClick}>
        {props.loading ? 'Loading...' : props.text}
      </button>
    </div>
  );
};
