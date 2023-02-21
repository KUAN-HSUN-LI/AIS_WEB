# AIS_WEB

## Prerequisite
1. Node.js >= 15
2. Python >= 3.8
## Installation
### Frontend
```
cd frontend
yarn
```
### Backend
```
cd backend
pip install -r requirement.txt
```

## Development
### Frontend
```
cd frontend
yarn run dev
```
### Backend
```
cd backend
uvicorn main:app --reload
```

### Deploy
1. Update the `VITE_HOST` and `VITE_BACKEND_PORT` values in the `frontend/.env.production` file.
2. Update the `VITE_HOST` and `GPU_INFO_DIR` values in the `backend/.env` file. Also change the `ENV` value to `prod`
3. Make sure the backend service in `docker-compose.yml` mount the correct path.
4. Deploy the site
```
docker-compose up -d --build
```