import * as React from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft } from 'lucide-react';
import { useParams } from 'react-router';
import { Spinner } from '~/components';
import { useCartStore } from '~/data';
import { Error } from '~/pages';
import { Artwork, ArtworkModel } from '~/api';
import './ArtDetail.scss';

export const ArtDetail = () => {
  const [artwork, setArtwork] = React.useState<Artwork | null>(null);
  const [selectedImageIndex, setSelectedImageIndex] = React.useState<number>(0);
  const [loading, setLoading] = React.useState(true);
  const [notFound, setNotFound] = React.useState(false);

  const { id } = useParams();
  const { cart, addToCart } = useCartStore();

  const spinnerTimeoutRef = React.useRef<number | null>(null);

  React.useEffect(() => {
    if (!id) return;
    setLoading(true);
    const startTime = Date.now();
    ArtworkModel.get(id)
      .then((res) => setArtwork(res.data))
      .catch((err) => {
        console.error(err);
        setNotFound(true);
      })
      .finally(() => {
        const elapsed = Date.now() - startTime;
        const remainingTime = Math.max(0, 300 - elapsed);
        spinnerTimeoutRef.current = setTimeout(() => setLoading(false), remainingTime);
      });
    return () => {
      if (spinnerTimeoutRef.current) clearTimeout(spinnerTimeoutRef.current);
    };
  }, [id]);

  if (loading) {
    return (
      <div className="ArtDetail">
        <div className="flex justify-center align-center w-100 pt-8">
          <Spinner />
        </div>
      </div>
    );
  }

  if (!artwork || notFound) return <Error />

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
                  selectedImageIndex === index ? ' ArtDetail__images__thumbnails__thumbnail--selected' : ''
                }`}
              >
                <img src={image.image} alt={artwork.title} />
              </div>
            ))}
          </div>
          <div className="ArtDetail__images__main">
            <img src={artwork.images[selectedImageIndex].image} alt={artwork.title} />
          </div>
        </div>
        <div className="ArtDetail__info">
          <h1 className="ArtDetail__info__title">{`"${artwork.title}" ${artwork.size}`}</h1>
          <p className="ArtDetail__info__price">
            {`${Number(artwork.price_cents / 100).toLocaleString('en-US', {
              style: 'currency',
              currency: 'USD',
            })} USD`}
          </p>
          <p className="ArtDetail__info__note">Shipping costs will be calculated at checkout.</p>
          <p className="ArtDetail__info__note">Unframed original {artwork.size} oil painting on canvas.</p>
          <p className="ArtDetail__info__note">Stephanie Bergeson, 2024-32</p>
          <p className="ArtDetail__info__note">
            * please contact us if you wish to receive a frame with this painting!
          </p>
          <button
            className="ArtDetail__info__button"
            onClick={() => addToCart(artwork)}
            disabled={cart.some((item) => item.id === artwork.id)}
          >
            {cart.some((item) => item.id === artwork.id) ? 'Added to Cart!' : 'Add to Cart'}
          </button>
        </div>
      </div>
    </div>
  );
};
