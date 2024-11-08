import { RouteObject } from 'react-router-dom';
import { About, ArtDetail, ArtList, CheckoutReturn, Gallery } from '~/pages';
import { Layout } from './layout';

export const routes: RouteObject[] = [
  {
    path: '/',
    element: <Layout />,
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
        path: '/checkout',
        element: <CheckoutReturn />,
      },
    ],
  },
];
