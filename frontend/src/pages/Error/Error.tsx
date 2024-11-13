import { Link } from 'react-router-dom';
import './Error.scss';

export const Error = () => {
  return (
    <div className="Error">
      <h2>Sorry, this page isn't available.</h2>
      <p>
        It may have been moved, or it may have never existed at all.
      </p>
      <Link to="/">Go Home</Link>
    </div>
  );
};
