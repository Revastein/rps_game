# Rock-Paper-Scissors

Rock-Paper-Scissors is a web application that allows users to play the classic game of Rock-Paper-Scissors online.
The application is built using FastAPI for the backend and Vue.js for the frontend.

## Backend

The backend of the application is built using FastAPI high-performance web framework for building
APIs with Python 3.10.

### Structure

- `rps_back`: Contains the backend code.
    - `rps_back/controllers`: Contains the controllers handling the business logic.
    - `rps_back/models`: Contains the database models and schemas.
    - `rps_back/routers`: Contains the API routers.
    - `rps_back/secure`: Contains the password hashing functions.
    - `rps_back/main.py`: Entry point of the backend application.

### Dependencies

- Python 3.10.x
- FastAPI
- SQLAlchemy
- Passlib

## Frontend

The frontend of the application is built using Vue.js, a JavaScript framework for building user interfaces.

### Structure

- `rps_front`: Contains the frontend code.
    - `rps_front/public`: Contains the static assets and HTML template.
    - `rps_front/src`: Contains the Vue.js components, styles, and scripts.

### Components

- `GameForm.vue`: Main interface of the game.
- `GameLobbyForm.vue`: Lobby interface where players make their choices.
- `LoginForm.vue`: Login form for users.
- `RegisterForm.vue`: Registration form for new users.
- `App.vue`: Root component of the Vue.js application.

### Scripts

- `rps_front/src/scripts`: Contains the scripts used by Vue.js components.

### Styles

- `rps_front/assets/css`: Contains the CSS styles for the frontend components.

## Usage

1. Clone the repository and navigate to the project directory.
2. Build the Docker containers using the provided `docker-compose.yml` file:

```bash
docker-compose up --build
```

1. Once the containers are up and running, you can access the application using the following URLs:

* Backend API: http://localhost:8000
* Frontend UI: http://localhost:8080

2. You can now register as a new user or login with existing credentials to start playing Rock-Paper-Scissors.

## License

This project is licensed under the MIT License.

## Autor

[Kovzel Yan](https://github.com/Revastein)
