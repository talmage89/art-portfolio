import * as Sentry from '@sentry/react';
import './Error.scss';

export const Error = () => {
  return (
    <div className="Error">
      <h2>An error occurred.</h2>
      <p>Please try again later.</p>
      <button className="Error__report" onClick={() => Sentry.showReportDialog()}>
        Report feedback
      </button>
    </div>
  );
};
