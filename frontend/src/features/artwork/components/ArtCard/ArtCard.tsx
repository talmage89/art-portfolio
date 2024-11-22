import * as React from 'react';
import { Artwork } from '~/api';
import { formatInches } from '~/utils/api';
import './ArtCard.scss';

type ArtCardProps = {
  artwork: Artwork;
  showInfo?: boolean;
  onClick?: () => void;
  dimensions?: [number, number];
};

export const ArtCard = ({ artwork, showInfo = true, onClick, dimensions }: ArtCardProps) => {
  const [srcLoaded, setSrcLoaded] = React.useState(false);

  return (
    <div className="ArtCard" onClick={onClick}>
      <div className="ArtCard__image">
        {dimensions && !srcLoaded && (
          <div
            className="ArtCard__image__dimensions"
            style={{
              width: '100%',
              paddingBottom: `${(dimensions[1] / dimensions[0]) * 100}%`,
            }}
          />
        )}
        <img
          style={srcLoaded ? {} : { display: 'none' }}
          alt={artwork.title}
          src={artwork.images[0]?.image}
          onLoad={() => setSrcLoaded(true)}
        />
      </div>
      {showInfo && (
        <>
          <h3 className="ArtCard__title">{`"${artwork.title}" ${formatInches(artwork.width_inches)}x${formatInches(
            artwork.height_inches
          )}`}</h3>
          {artwork.status === 'coming_soon' && <p className="ArtCard__comingSoon">Coming Soon!</p>}
          <p className="ArtCard__price">
            {Number(artwork.price_cents / 100).toLocaleString('en-US', {
              style: 'currency',
              currency: 'USD',
            })}
          </p>
        </>
      )}
    </div>
  );
};
