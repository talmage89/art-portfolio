import { Artwork } from "~/api";
import "./ArtCard.scss";

type ArtCardProps = {
  artwork: Artwork;
  showInfo?: boolean;
  onClick?: () => void;
};

export const ArtCard = ({
  artwork,
  showInfo = true,
  onClick,
}: ArtCardProps) => {
  return (
    <div className="ArtCard" onClick={onClick}>
      <div className="ArtCard__image">
        <img src={artwork.images[0].image} alt={artwork.title} />
      </div>
      {showInfo && (
        <>
          <h3 className="ArtCard__title">{`"${artwork.title}" ${artwork.size}`}</h3>
          <p className="ArtCard__price">
            {Number(artwork.price_cents / 100).toLocaleString("en-US", {
              style: "currency",
              currency: "USD",
            })}
          </p>
        </>
      )}
    </div>
  );
};
