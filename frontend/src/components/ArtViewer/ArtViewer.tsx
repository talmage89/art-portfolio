import { X } from "lucide-react";
import { Artwork } from "~/api";
import "./ArtViewer.scss";

type ArtViewerProps = {
  artwork: Artwork | null;
  open: boolean;
  onClose: () => void;
};

export const ArtViewer = ({ artwork, open, onClose }: ArtViewerProps) => {
  if (!open || !artwork) return null;

  return (
    <div className="ArtViewer" onClick={onClose}>
      <div className="ArtViewer__content" onClick={(e) => e.stopPropagation()}>
        <div className="ArtViewer__close" onClick={onClose}>
          <X />
        </div>
        <div className="ArtViewer__image">
          <img src={artwork.images[0].image} alt={artwork.title} />
        </div>
        <h2 className="ArtViewer__title">{artwork.title}</h2>
      </div>
    </div>
  );
};
