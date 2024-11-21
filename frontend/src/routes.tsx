import * as Sentry from '@sentry/react';
import { RouteObject } from 'react-router-dom';
import { Layout } from '~/layout';
import { About, ArtDetail, ArtList, CheckoutReturn, Gallery, Error, NotFound, HealthCheck } from '~/pages';

const LayoutWithBoundary = Sentry.withErrorBoundary(Layout, {
  fallback: <Error />,
});

export const routes: RouteObject[] = [
  {
    path: '/',
    element: <LayoutWithBoundary />,
    children: [
      {
        path: '/',
        element: <ArtList />,
      },
      {
        path: '/about',
        element: <About />,
      },
      {
        path: '/gallery',
        element: <Gallery />,
      },
      {
        path: '/art/:id',
        element: <ArtDetail />,
      },
      {
        path: '/checkout/success',
        element: <CheckoutReturn />,
      },
      {
        path: '/health',
        element: <HealthCheck />,
      },
      {
        path: '*',
        element: <NotFound />,
      },
    ],
  },
];
