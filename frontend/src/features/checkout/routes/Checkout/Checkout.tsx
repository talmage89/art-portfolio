import * as React from 'react';
import { useSearchParams } from 'react-router-dom';
import { http } from '~/api';
import { useCartStore } from '~/data/stores';
import { useToast } from '~/data/toast';
import { Cart, CheckoutForm, CheckoutFormData, CheckoutReturn } from '~/features/checkout';
import './Checkout.scss';

enum CHECKOUT_PAGES {
  cart = 'cart',
  checkout = 'checkout',
  success = 'success',
}

export const Checkout = () => {
  const [step, setStep] = React.useState<CHECKOUT_PAGES>(CHECKOUT_PAGES.cart);
  const [loading, setLoading] = React.useState(false);

  const { cart } = useCartStore();
  const [searchParams] = useSearchParams();
  const { errorToast } = useToast();

  React.useEffect(() => {
    const success = searchParams.get('success');
    success && setStep(CHECKOUT_PAGES.success);
  }, [searchParams]);

  function handleCheckout(data: CheckoutFormData) {
    setLoading(true);
    http
      .post('/api/create-checkout-session/', { product_ids: cart.map((item) => item.id), shipping_details: data })
      .then((res) => {
        window.location.href = res.data.url;
      })
      .catch((err) => {
        const data = err.response.data;
        if (data?.includes('SHIPPING ERROR')) {
          try {
            const message = (Object.values(JSON.parse(data.split('\n')[1]))[0] as string[])[0];
            errorToast(message);
          } catch (e) {
            errorToast('There was an error with your shipping details. Please try again.');
          }
        } else {
          errorToast(data);
        }
      })
      .finally(() => setLoading(false));
  }

  return (
    <div className="Checkout">
      {step === CHECKOUT_PAGES.cart && <Cart onProceed={() => setStep(CHECKOUT_PAGES.checkout)} />}
      {step === CHECKOUT_PAGES.checkout && (
        <CheckoutForm
          createSessionLoading={loading}
          onBack={() => setStep(CHECKOUT_PAGES.cart)}
          onSubmit={(data) => handleCheckout(data)}
        />
      )}
      {step === CHECKOUT_PAGES.success && <CheckoutReturn />}
    </div>
  );
};
