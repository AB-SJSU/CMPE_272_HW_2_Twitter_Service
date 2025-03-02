# CMPE_272_HW_2_Twitter_Service
Service that interacts with the Mastodon API to programmatically create, retrieve, and delete posts.

## Step 1: Create Mastodon Account 
- get MASTODON_API_URL and TOKEN_URL and update the values in backend/env file

## step 2: Install backend dependencies
- create venv for backend `python3 -m venv venv` and run `pip install -r backend/requirements.txt` in terminal

## Step 3: Start Backend APIs
- go to backend directory and run `python3 run.py`

## Step 4: Install necessary npm packages for frontend
- go to directory frontend/mastodon_twitter_app
- run `npm install` in terminal
- update and confirm env file variables for frontend

## step 5: Run Next.js app
- run `cd frontend/mastodon_twitter_app && npm start` in terminal

### How to run tests for backend APIs
- go to backend directory and run `pytest`
