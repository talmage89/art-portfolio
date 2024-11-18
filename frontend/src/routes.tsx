import { RouteObject } from 'react-router-dom';
import { ErrorBoundary } from 'react-error-boundary';
import { Layout } from '~/layout';
import { About, ArtDetail, ArtList, CheckoutReturn, Gallery, Error, NotFound, HealthCheck } from '~/pages';

export const routes: RouteObject[] = [
  {
    path: '/',
    element: (
      <ErrorBoundary FallbackComponent={Error}>
        <Layout />
      </ErrorBoundary>
    ),
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
