import * as React from 'react';
import { ArtCard, ArtViewer, Spinner } from '~/components';
import { Artwork, ArtworkModel } from '~/api';
import './Gallery.scss';

export const Gallery = () => {
  const [openArtwork, setOpenArtwork] = React.useState<Artwork | null>(null);
  const [artworks, setArtworks] = React.useState<Artwork[]>([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    setLoading(true);
    ArtworkModel.list()
      .then((res) => setArtworks(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const renderArtwork = (artwork: Artwork) => {
    return (
      <ArtCard
        key={artwork.id}
        artwork={artwork}
        showInfo={false}
        onClick={() => setOpenArtwork(artwork)}
        dimensions={artwork.image_dimensions}
      />
    );
  };

  return (
    <div className="Gallery">
      {loading ? (
        <div className="flex justify-center align-center w-100 pt-8">
          <Spinner />
        </div>
      ) : artworks.length > 0 ? (
        <>
          <div className="Gallery__left">{artworks.filter((_, i) => i % 2 === 0).map(renderArtwork)}</div>
          <div className="Gallery__right">{artworks.filter((_, i) => i % 2 === 1).map(renderArtwork)}</div>
          <ArtViewer artwork={openArtwork} open={!!openArtwork} onClose={() => setOpenArtwork(null)} />
        </>
      ) : (
        <div className="Gallery__empty">
          <p>No paintings found</p>
        </div>
      )}
    </div>
  );
};
