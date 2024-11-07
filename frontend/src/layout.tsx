import * as React from "react";
import { Outlet } from "react-router";
import { ShoppingCart } from "lucide-react";
import { Cart, Navbar } from "~/components";
import { useCartStore } from "~/data";
import "./index.scss";

export const Layout = () => {
  const [cartOpen, setCartOpen] = React.useState(false);

  const { cart, setCart } = useCartStore();

  React.useEffect(() => {
    const cartJSON = localStorage.getItem("cart");
    const cart = cartJSON ? JSON.parse(cartJSON) : [];
    cart.length && setCart(cart);
  }, []);

  React.useEffect(() => {
    cart.length && localStorage.setItem("cart", JSON.stringify(cart));
  }, [cart]);

  return (
    <div className="Layout">
      <Navbar />
      <div className="Layout__cartBadge" onClick={() => setCartOpen(true)}>
        <div className="Layout__cartBadge__data">
          <ShoppingCart className="Layout__cartBadge__data__icon" />
          <p className="Layout__cartBadge__data__count">{cart.length}</p>
        </div>
      </div>
      <div className="Layout__content">
        <Outlet />
      </div>
      <Cart items={cart} isOpen={cartOpen} onClose={() => setCartOpen(false)} />
    </div>
  );
};
