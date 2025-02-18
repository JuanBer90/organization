# Organization Chart Backend

**Description**: This is the backend for the Organization Chart application, built with FastAPI.

## Requirements

- Docker: Install Docker from [here](https://docs.docker.com/get-docker/).
- Docker Compose: Install Docker Compose from [here](https://docs.docker.com/compose/install/).


## Docker

- Make sure to run the following command in the **root directory** of the project:

  ```
  docker compose up --build
  ```

- **API Docs available at**:
- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)


# Organization Chart Frontend

This is the frontend of the Organization Chart application, built with Vite + React.

## Frontend Requirements

- Node.js v18.18.2: Install Node.js using NVM (Node Version Manager)

  1. Install NVM (if you don't have it already) by following the instructions [here](https://github.com/nvm-sh/nvm#installing-and-updating).
  
  2. Install Node.js v18.18.2:
     ```
     nvm install 18.18.2
     ```
     
  3. Use Node.js v18.18.2:
     ```
     nvm use 18.18.2
     ```
     
## Getting Started

1. Install Dependencies:
   Run the following command to install all dependencies:
   
   `npm install`

2. Run the Development Server:
   Start the application with:
   
   `npm run dev`

   By default, the app runs on http://localhost:5173.


## License

MIT


