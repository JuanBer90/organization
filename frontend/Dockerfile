# Use Node.js base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Expose the port used by Vite
EXPOSE 5173

# Start the frontend application
CMD ["npm", "run", "dev", "--", "--host"]
