import * as React from "react";
import { useNavigate } from "react-router-dom";
import { ArtCard } from "~/components";
import { Artwork, ArtworkModel } from "~/api";
import { mockArtworks } from "~/data";
import "./ArtList.scss";

export const ArtList = () => {
  const [artworks, setArtworks] = React.useState<Artwork[]>([]);

  const navigate = useNavigate();

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
        onClick={() => navigate(`/art/${artwork.id}`)}
      />
    );
  };

  return (
    <div className="ArtList">
      <div className="ArtList__left">
        {artworks.filter((_, i) => i % 2 === 0).map(renderArtwork)}
      </div>
      <div className="ArtList__right">
        {artworks.filter((_, i) => i % 2 === 1).map(renderArtwork)}
      </div>
    </div>
  );
};
