FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10 AS backend-build

EXPOSE 8000

WORKDIR /app

COPY backend/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM node:lts-alpine AS frontend-build

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ .

CMD ["npm", "run", "serve"]
