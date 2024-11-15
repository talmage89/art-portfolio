import { RouteObject } from 'react-router-dom';
import { ErrorBoundary } from 'react-error-boundary';
import { About, ArtDetail, ArtList, CheckoutReturn, Gallery, Error, NotFound } from '~/pages';
import { Layout } from '~/layout';

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
        path: '*',
        element: <NotFound />,
      },
    ],
  },
];
