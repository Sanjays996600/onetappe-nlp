# Deployment Notes

## Backend
- Runs on port 8000 by default.
- Use `.env` file in `/backend/` directory to configure environment variables.
- Important variables:
  - `DATABASE_URL`: Database connection string.
  - `JWT_SECRET_KEY`: Secret key for JWT authentication.
- To run backend:
  ```bash
  uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
  ```

## Frontend
- Uses environment variable `API_BASE_URL` to connect to backend API.
- Use `.env` file in `/frontend/` directory to configure environment variables.
- To run frontend:
  ```bash
  npm start
  ```

## CORS
- Ensure backend CORS settings allow requests from frontend origin during development and production.
- Configure CORS middleware in backend if needed.