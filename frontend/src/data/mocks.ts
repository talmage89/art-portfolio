import { Artwork } from "~/api";

export const mockArtworks: Artwork[] = [
  {
    id: "0",
    title: "View from Lauritzen",
    size: "6x8",
    price_cents: 18000,
    images: [
      {
        id: "0-0",
        image:
          "https://format.creatorcdn.com/9aea48ef-8147-45cf-85c8-2b356e59056f/0/0/0/0,0,3423,2584,550,415/0-0-0/86a0231c-676d-4206-857a-afa28fc86bcf/1/2/View+from+Lauritzen.JPG?fjkss=exp=2046445165~hmac=3a8952dee065d5265c763599eb15430ade44d176514e1d91ccfabbd8d2798c3b&550",
        is_main_image: true,
        uploaded_at: new Date().toISOString(),
      },
      {
        id: "0-1",
        image:
          "https://format.creatorcdn.com/9aea48ef-8147-45cf-85c8-2b356e59056f/0/0/0/0,0,3329,2657,900,2657/0-0-0/db1ef415-1e0e-4971-b8f7-cab6d8aea4b8/1/1/View+from+Lauritzen+framed.JPG?fjkss=exp=2046443370~hmac=91634ee3fbb85cc042b497513d6b5d1e8fd1b3bb2fcfd2d035f703646be30122",
        is_main_image: false,
        uploaded_at: new Date().toISOString(),
      },
    ],
    status: "active",
    creation_date: new Date().toISOString(),
  },
  {
    id: "1",
    title: "Willow Pond Jordan River Trail",
    size: "5x7",
    price_cents: 15000,
    images: [
      {
        id: "1-0",
        image:
          "https://format.creatorcdn.com/9aea48ef-8147-45cf-85c8-2b356e59056f/0/0/0/0,0,1806,2486,550,757/0-0-0/648b28e3-8490-43bf-b0e6-0d77ed464146/1/2/Willow+Pond+Park+JRT.JPG?fjkss=exp=2046444860~hmac=0828b798051fb7d72c6cd98298ee5fa794502f3ff683f37c8dbf0e9c05ba9411&550",
        is_main_image: true,
        uploaded_at: new Date().toISOString(),
      },
    ],
    status: "active",
    creation_date: new Date().toISOString(),
  },
  {
    id: "2",
    title: "Arrowhead Park Jordan River Trail",
    size: "5x7",
    price_cents: 15000,
    images: [
      {
        id: "2-0",
        image:
          "https://format.creatorcdn.com/9aea48ef-8147-45cf-85c8-2b356e59056f/0/0/0/0,0,3041,2269,3041,1200/0-0-0/f9b07ad6-179f-4eab-9020-5dcbc9e9d830/1/1/Kidney+Pond+JRT.JPG?fjkss=exp=2046258489~hmac=d3a39c0c4acaa7774a52bfa22629a396d2ce40c7f39dfeec460711320c33908d",
        is_main_image: true,
        uploaded_at: new Date().toISOString(),
      },
    ],
    status: "active",
    creation_date: new Date().toISOString(),
  },
];
