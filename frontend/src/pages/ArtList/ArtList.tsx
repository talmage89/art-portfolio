import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArtCard, Spinner } from '~/components';
import { Artwork, ArtworkModel } from '~/api';
import './ArtList.scss';

export const ArtList = () => {
  const [artworks, setArtworks] = React.useState<Artwork[]>([]);
  const [loading, setLoading] = React.useState(true);

  const navigate = useNavigate();

  React.useEffect(() => {
    setLoading(true);
    ArtworkModel.list({ status: ["available", "coming_soon"] })
      .then((res) => setArtworks(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const renderArtwork = (artwork: Artwork) => {
    return (
      <ArtCard
        key={artwork.id}
        artwork={artwork}
        onClick={() => navigate(`/art/${artwork.id}`)}
        dimensions={artwork.image_dimensions}
      />
    );
  };

  return (
    <div className="ArtList">
      {loading ? (
        <div className="flex justify-center align-center w-100 pt-8">
          <Spinner />
        </div>
      ) : artworks.length > 0 ? (
        <>
          <div className="ArtList__left">{artworks.filter((_, i) => i % 2 === 0).map(renderArtwork)}</div>
          <div className="ArtList__right">{artworks.filter((_, i) => i % 2 === 1).map(renderArtwork)}</div>
        </>
      ) : (
        <div className="ArtList__empty">
          <p>No paintings found</p>
        </div>
      )}
    </div>
  );
};
