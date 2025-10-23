# Lab 2 Writeup

## Overview

In this Lab2 exercise, we have following tasks: 1. apply LLM model to add translating feature and note generating feature; 2. modify the code to store data in an external database; 3. deploy the app on vercel. In this markdown file, we will go through these tasks step by step and discuss the dificulty encountered.


## LLM Model Application

### What was done
- Selected model and got the api key from github.com/marketplace/models. 
- Saved the api key in .env file which was not committed to version control. 
- Wrote core part of the code to guide AI. 
- Added translating feature and note generating feature using vibe coding.
  
The note generating feature allows the users to input natural language and choose the output language they want. We also help the users extract three tags, event date and event time.

### Challenge Encounter
The difficulty of this part was guiding the AI agent to form the ideal frontend.  

<img width="415" height="288" alt="image" src="https://github.com/user-attachments/assets/134122a4-aa10-44db-9c57-956d1675dcfc" />  

At first the tags, event date and event time was shown inside the content.  

<img width="372" height="91" alt="image" src="https://github.com/user-attachments/assets/6974366e-a523-479a-a2ac-8c12d68e7457" />  

Then I tried to describe my requirement again.  

<img width="415" height="318" alt="image" src="https://github.com/user-attachments/assets/ea3f136c-0786-455f-aef9-af9ecda84e2a" />  

Still not what I wanted.  

The problem was finally solved by giving the AI agent an example image.  

<img width="453" height="416" alt="image" src="https://github.com/user-attachments/assets/f5c58995-500e-4bc4-b761-14e28e87909b" />


## Refactor to External Database

Refactored the application to use PostgreSQL hosted on Supabase.

### Database Refactoring Steps

<img width="356" height="180" alt="image" src="https://github.com/user-attachments/assets/fc33d5f9-703b-4d19-a3f3-a94b704f12d5" />

- Update Database Configuration (`src/main.py`)

- Add PostgreSQL Driver (`requirements.txt`)

Added the PostgreSQL driver:
```
psycopg[binary]==3.2.3
```

### Supabase Setup

- Create Supabase Project

1. Go to [Supabase](https://supabase.com)
2. Create a new project

- Get Connection String

1. Navigate to **Connection string**
2. Select **pooled** connection string
3. Copy the connection string 

<img width="2030" height="980" alt="image" src="https://github.com/user-attachments/assets/1a3d68e2-dd26-493e-aecc-e4bd2095aeb8" />


### Testing 

<img width="2908" height="1238" alt="image" src="https://github.com/user-attachments/assets/3b78c280-b55a-4860-9695-50bbce2ee7b3" />


## Vercel Deployment

### What was done

1. Asked AI agent to help modify the code for vercel deployment.
2. Go to Vercel Dashboard
3. Select our project and set up
4. Navigate to **Settings** → **Environment Variables**
5. Add the following variables:

   - **Name**: `DATABASE_URL`
   - **Value**: Paste the Supabase connection string
   
   - **Name**: `SECRET_KEY`
   - **Value**: A random secret string

### Challenge Encounter
The direct connection of the supabase connection string was used at first, the deployment failed with error 500. With the suggestion from deepseek, the supabase database url was changed into pool connection and ssl mode was used. After that the deployment works well.




## Lesson Learnt

- When an AI model fails to provide us with the desired results, we can switch to another AI model for assistance
- Providing images for AI agents can help them better understand the frontend we want




