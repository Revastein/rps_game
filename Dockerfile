FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10 AS backend-build

EXPOSE 8000

WORKDIR /app

COPY rps_back/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /rps_back .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM node:lts-alpine AS frontend-build

WORKDIR /app

COPY rps_front/package*.json ./

RUN npm install

COPY ../pet_projects/rps_game/rps_front .

CMD ["npm", "run", "serve"]