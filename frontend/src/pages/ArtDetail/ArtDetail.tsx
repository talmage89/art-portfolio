import * as React from "react";
import { Link } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import { useParams } from "react-router";
import { mockArtworks, useCartStore } from "~/data";
import { Artwork, ArtworkModel } from "~/api";
import "./ArtDetail.scss";

export const ArtDetail = () => {
  const [artwork, setArtwork] = React.useState<Artwork | null>(null);
  const [selectedImageIndex, setSelectedImageIndex] = React.useState<number>(0);

  const { id } = useParams();
  const { cart, addToCart } = useCartStore();

  React.useEffect(() => {
    if (!id) return;
    if (import.meta.env.VITE_USE_BACKEND === "true") {
      ArtworkModel.get(id).then((res) => {
        setArtwork(res.data);
      });
    } else {
      setArtwork(mockArtworks.find((artwork) => artwork.id === id) || null);
    }
  }, [id]);

  if (!artwork) return null;

  return (
    <div className="ArtDetail">
      <Link to="/" className="ArtDetail__back">
        <ChevronLeft />
        <p>Back to Store</p>
      </Link>
      <div className="ArtDetail__main">
        <div className="ArtDetail__images">
          <div className="ArtDetail__images__thumbnails">
            {artwork.images.map((image, index) => (
              <div
                key={index}
                onClick={() => setSelectedImageIndex(index)}
                className={`ArtDetail__images__thumbnails__thumbnail${
                  selectedImageIndex === index
                    ? " ArtDetail__images__thumbnails__thumbnail--selected"
                    : ""
                }`}
              >
                <img src={image.image} alt={artwork.title} />
              </div>
            ))}
          </div>
          <div className="ArtDetail__images__main">
            <img
              src={artwork.images[selectedImageIndex].image}
              alt={artwork.title}
            />
          </div>
        </div>
        <div className="ArtDetail__info">
          <h1 className="ArtDetail__info__title">{`"${artwork.title}" ${artwork.size}`}</h1>
          <p className="ArtDetail__info__price">
            {`${Number(artwork.price_cents / 100).toLocaleString("en-US", {
              style: "currency",
              currency: "USD",
            })} USD`}
          </p>
          <p className="ArtDetail__info__note">
            Shipping costs will be calculated at checkout.
          </p>
          <p className="ArtDetail__info__note">
            Unframed original {artwork.size} oil painting on canvas.
          </p>
          <p className="ArtDetail__info__note">Stephanie Bergeson, 2024-32</p>
          <p className="ArtDetail__info__note">
            * please contact us if you wish to receive a frame with this
            painting!
          </p>
          <button
            className="ArtDetail__info__button"
            onClick={() => addToCart(artwork)}
            disabled={cart.some((item) => item.id === artwork.id)}
          >
            {cart.some((item) => item.id === artwork.id)
              ? "Added to Cart!"
              : "Add to Cart"}
          </button>
        </div>
      </div>
    </div>
  );
};
