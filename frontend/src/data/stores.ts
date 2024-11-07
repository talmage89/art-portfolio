import { create } from "zustand";
import { Artwork } from "~/api";

type CartStore = {
  cart: Artwork[];
  setCart: (cart: Artwork[]) => void;
  addToCart: (artwork: Artwork) => void;
  removeFromCart: (productId: string) => void;
};

export const useCartStore = create<CartStore>((set) => ({
  cart: [],
  setCart: (cart: Artwork[]) => set({ cart }),
  addToCart: (product) => set((state) => ({ cart: [...state.cart, product] })),
  removeFromCart: (productId: string) =>
    set((state) => ({
      cart: state.cart.filter((item) => item.id !== productId),
    })),
}));
