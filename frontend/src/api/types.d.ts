export type Artwork = {
  id: string;
  title: string;
  size: string;
  price_cents: number;
  images: Image[];
  status: string;
  creation_date: string;
};

export type Image = {
  id: string;
  image: string;
  is_main_image: boolean;
  uploaded_at: string;
};
