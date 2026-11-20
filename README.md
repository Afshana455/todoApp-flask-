# Todo App

A simple and intuitive Todo application built with **Flask** for the backend and **Vue.js** for the frontend. The application allows users to manage their daily tasks by creating, viewing, updating, and deleting todos through a responsive user interface.

## Features

- **Add Tasks** – Create new todo items with task descriptions.
- **View Tasks** – Display all added tasks in an organized list.
- **Update Tasks** – Edit existing task details.
- **Mark as Completed** – Track completed and pending tasks.
- **Delete Tasks** – Remove tasks that are no longer needed.
- **REST API** – Flask backend provides API endpoints for frontend communication.
- **Responsive UI** – Vue.js frontend provides a smooth and interactive experience.

## Tech Stack

### Backend
- Python
- Flask
- Flask REST API

### Frontend
- Vue.js
- JavaScript
- HTML
- CSS



## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/todos` | Retrieve all todos |
| POST | `/api/todos` | Create a new todo |
| PUT | `/api/todos/<id>` | Update an existing todo |
| DELETE | `/api/todos/<id>` | Delete a todo |

## How It Works

1. The user interacts with the Vue.js frontend.
2. Vue sends HTTP requests to the Flask backend using the REST API.
3. Flask processes the requests and manages todo data.
4. The backend returns responses in JSON format.
5. Vue updates the UI dynamically based on the response.

