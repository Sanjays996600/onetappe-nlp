#!/bin/bash

# OneTappe NLP Debug UI Setup Script

echo "Setting up OneTappe NLP Debug UI..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Start the development server
echo "Starting development server..."
echo "The UI will be available at http://localhost:3000"
echo "Make sure the NLP API is running at http://localhost:5000"
npm start