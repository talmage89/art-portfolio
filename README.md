# Art Portfolio

## Overview

Tech Stack:

- Frontend: Vite, React, Typescript
- Backend: Django, Django REST Framework, Docker, PostgreSQL
- Vendor integrations: Stripe, Mailgun, Shippo

## Development

To start the frontend, you will need node installed:

```bash
cd frontend
npm install
npm start
```

To start the backend, you will need python and docker installed:

```bash
cd backend
docker compose up -d
python -m venv venv
source venv/bin/activate
pip install pip-tools
pip-compile --upgrade requirements.in
pip-sync requirements.txt
python manage.py runserver
```

## Deployment

To deploy the application, run the following on the server in the repo root. Make sure you have pip-tools installed.

```bash
bash ./server/deploy.sh
```

## Environment Variables

### General

Create a `.env` file in the root of the frontend directory with the following data:

```
# frontend .env
VITE_API_HOST=http://localhost:8000/
```

### Stripe

For Stripe, you will need to create an account and get an API key. Put the publishable key in the frontend `.env` file:

```
# frontend .env
VITE_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
```

And put the secret key in an `.env` file in the root of the backend directory:

```
# backend .env
STRIPE_SECRET_KEY=your_stripe_secret_key
```

To have Stripe watch for payment/checkout events locally, you will need the Stripe CLI installed. Visit [Stripe CLI](https://stripe.com/docs/stripe-cli) for installation instructions.

Once the CLI is installed run the following to start the webhook listener:

```bash
stripe login
stripe listen --forward-to localhost:8000/webhook
```

Then add the webhook signing secret to the backend `.env` file:

```
# backend .env
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

## Stripe Checkout

To test the checkout flow, you can use the following test card numbers:

- Payment Success: 4242 4242 4242 4242
- Payment Failure: 4000 0000 0000 9987
