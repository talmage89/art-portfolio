# Art Portfolio

## Development

To start the frontend:

```bash
cd frontend
npm install
npm start
```

To start the backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

On the frontend, to use backend instead of dummy data, create a `.env` file in the root of the frontend directory with the following data:

```
VITE_API_HOST=http://localhost:8000/
VITE_USE_BACKEND=true
```
