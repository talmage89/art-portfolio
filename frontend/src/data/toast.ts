import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const useToast = () => {
  const showInfo = (message: string) => {
    toast.info(message, {
      position: 'bottom-center',
      autoClose: 3000,
      hideProgressBar: true,
      closeOnClick: true,
    });
  };

  const showError = (message: string) => {
    toast.error(message, {
      position: 'bottom-center',
      autoClose: 5000,
      hideProgressBar: true,
      closeOnClick: true,
    });
  };

  return {
    toast: showInfo,
    errorToast: showError,
  };
};
