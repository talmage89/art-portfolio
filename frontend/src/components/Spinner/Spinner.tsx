import './Spinner.scss';

type SpinnerProps = {
  width?: number;
  height?: number;
  text?: string;
};

export const Spinner = ({ width = 64, height = 64, text }: SpinnerProps) => {
  return (
    <div className="Spinner">
      <div className="Spinner__circle" style={{ width: `${width}px`, height: `${height}px` }} />
      {text && <p>{text}</p>}
    </div>
  );
};
