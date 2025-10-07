export type Artwork = {
  id: string;
  title: string;
  painting_number: number;
  painting_year: number;
  width_inches: number;
  height_inches: number;
  paper: boolean;
  medium: string;
  category: string;
  status: string;
  price_cents: number;
  created_at: string;
  updated_at: string;
  images: Image[];
  image_dimensions?: [number, number];
};

export type Image = {
  id: string;
  image: string;
  is_main_image: boolean;
  uploaded_at: string;
};
