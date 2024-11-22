import * as Sentry from '@sentry/react';
import { RouteObject } from 'react-router-dom';
import { Layout } from '~/layout';
import { About } from '~/features/about';
import { ArtDetail, ArtList, Gallery } from '~/features/artwork';
import { Checkout } from '~/features/checkout';
import { Error, NotFound, HealthCheck } from '~/features/core';

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
        path: '/cart',
        element: <Checkout />,
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
