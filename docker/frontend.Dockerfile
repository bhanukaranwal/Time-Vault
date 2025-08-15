# Use an official Node runtime as a parent image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the frontend source code
COPY ./frontend /app

# Expose the port the app runs on
EXPOSE 3000

# Command to run the app
CMD ["npm", "start"]