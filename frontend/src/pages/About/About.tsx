import * as React from 'react';
import './About.scss';

import about_img from '~/assets/cc65d761-1ea5-41c6-a9fe-c14d4a5d0ab9.jpg';

export const About = () => {
  const [imageLoaded, setImageLoaded] = React.useState(false);

  return (
    <div className="About">
      <div className="About__hero">
        <div className="About__hero__image">
          {!imageLoaded && (
            <div 
              className="About__hero__image__placeholder" 
              style={{ aspectRatio: '569/319' }}
            />
          )}
          <img 
            src={about_img} 
            alt="Stephanie Bergeson"
            style={{ display: imageLoaded ? 'block' : 'none' }}
            onLoad={() => setImageLoaded(true)}
          />
        </div>
        <div className="About__hero__info">
          <h2 className="About__hero__info__title">Stephanie Bee Studio</h2>
          <p className="About__hero__info__subtitle">Connect with me on Instagram!</p>
          <p className="About__hero__info__handle">
            <a href="https://www.instagram.com/stephanie_bee_studio" target="_blank" rel="noopener noreferrer">
              @stephanie_bee_studio
            </a>
          </p>
        </div>
      </div>
      <div className="About__content">
        <div className="About__content__section">
          <h3 className="About__content__section__title">Biography</h3>
          <p className="About__content__section__text">
            I was born and raised in Canada, near the rocky mountains. As an adult I have lived in several states
            including Hawaii, Louisiana, Virginia, and Texas. While there were things I enjoyed about each of these
            places, I'm happy I found my way back to the mountains, this time in Utah. I love hiking, camping and rock
            climbing and just enjoying the beautiful outdoors with my husband and four children.
          </p>
        </div>
        <div className="About__content__section">
          <h3 className="About__content__section__title">My Beginnings in Art</h3>
          <p className="About__content__section__text">
            I have always loved to draw and remember being very inspired as a 5 year old, overhearing a proud grandma
            brag about how her grandson could draw whatever he wanted just from his imagination. As a teen I took
            lessons from a watercolor artist in my community, Rene Hill. As I approached college I was incredibly
            intimidated by the idea of submitting a portfolio and got my bachelor's degree in history and German
            instead.
          </p>
        </div>
        <div className="About__content__section">
          <h3 className="About__content__section__title">Recent Developments</h3>
          <p className="About__content__section__text">
            I started studying art more seriously in 2022 after my youngest son was born. I've had the privilege of
            learning from artists like Emily Fox King, Andrew Payne, and Kirk Richards at the J. Kirk Richards Studio
            Academy over the past few years.
            <br />
            <br />I have learned to love oil painting, and how a painting can communicate a feeling in a way words
            can't. My painting practice has become a refuge for me from the wonderful chaos that is raising children. It
            helps me to recharge, and step back to see the beauty in the commotion of my day to day life.
          </p>
        </div>
      </div>
    </div>
  );
};
