import * as React from "react";
import { ArtCard, ArtViewer } from "~/components";
import { Artwork, ArtworkModel } from "~/api";
import { mockArtworks } from "~/data";
import "./Gallery.scss";

export const Gallery = () => {
  const [openArtwork, setOpenArtwork] = React.useState<Artwork | null>(null);
  const [artworks, setArtworks] = React.useState<Artwork[]>([]);

  React.useEffect(() => {
    if (import.meta.env.VITE_USE_BACKEND === "true") {
      ArtworkModel.list().then((res) => {
        setArtworks(res.data);
      });
    } else {
      setArtworks(mockArtworks);
    }
  }, []);

  const renderArtwork = (artwork: Artwork) => {
    return (
      <ArtCard
        key={artwork.id}
        artwork={artwork}
        showInfo={false}
        onClick={() => setOpenArtwork(artwork)}
      />
    );
  };

  return (
    <div className="Gallery">
      <div className="Gallery__left">
        {artworks.filter((_, i) => i % 2 === 0).map(renderArtwork)}
      </div>
      <div className="Gallery__right">
        {artworks.filter((_, i) => i % 2 === 1).map(renderArtwork)}
      </div>
      <ArtViewer
        artwork={openArtwork}
        open={!!openArtwork}
        onClose={() => setOpenArtwork(null)}
      />
    </div>
  );
};
