# Journal App

Release your feelings with Journal App.

## Features
- Create a new journal entry (title, content, date)
- View all entries as teasers

## Tech Stack
- Frontend: Vue.js + Vue Router
- Backend: FastAPI
- Database: MongoDB

## Setup

### Backend
1. Install dependencies:
pip install fastapi pymongo uvicorn
  or: python3 -m pip install fastapi
  python3 -m pip install uvicorn
2. Run the server:
uvicorn main:app --reload
or: python3 -m uvicorn main:app --reload

## MongoDB
To add your MongoDB URI string securely:

Create a .env file in your backend directory:
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority

Optional: Install python-dotenv:
pip install python-dotenv

### Frontend
1. Install dependencies:
npm install

2. Run the app:
npm run dev
