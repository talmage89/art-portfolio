import { useCallback } from 'react';

declare global {
  interface Window {
    goatcounter: {
      count: (opts: { path: string; event?: boolean; title?: string; referrer?: string }) => void;
    };
  }
}

export const useTrackClick = (eventName: string) => {
  return useCallback(
    (name?: string) => {
      if (typeof window !== 'undefined' && window.goatcounter) {
        window.goatcounter.count({
          path: eventName,
          event: true,
          title: name,
        });
      }
    },
    [eventName]
  );
};
