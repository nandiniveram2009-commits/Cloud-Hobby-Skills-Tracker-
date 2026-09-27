
# Online Hobby & Skills Tracker with Community Sharing on Cloud




## Overview 

The Online Hobby & Skills Tracker with Community Sharing on Cloud is an enterprise-grade, cloud-backed platform designed to help users structure deliberate practice, track milestones, maintain active calendar streaks, and share achievements with an interactive community feed. Built as a comprehensive cloud computing project, it demonstrates full-stack development, cloud persistence, object storage, RESTful API design, and cloud security best practices.

## Problem statement 

Most individuals abandon hobbies and skill development due to:


-A lack of structured tracking and measurable accountability.
-Inability to visualize incremental progress over time.
Isolation and a lack of social reinforcement or community motivation



##  Objectives 

-Build a scalable, cloud-hosted full-stack application.

-Implement secure authentication and user-specific data isolation.

-Integrate cloud-managed NoSQL/SQL databases and object storage.

-Provide automated analytics, streak calculation engines, and interactive charts.

-Deliver a social community feed complete with real-time likes and comments.



## Features

-User Accounts & Profiles: Secure registration, login, profile bio updates, and custom avatar uploads via cloud object storage.

-Hobby & Skill Management: Create, update, and categorize skills (Music, Coding, Art, Fitness, etc.) with proficiency levels.

-Goal & Milestone Tracking: Set quantitative targets (e.g., practice 30 hours) with automated progress calculations and milestone completions.

-Practice Session Logging: Log practice duration, activities, and notes with automatic streak and time aggregations.

-Cloud Object Storage: Secure binary file uploads (images, certificates) stored in cloud buckets with metadata pointers.

-Community Feed: Share achievement posts with optional media proof, visible to the global community.

-Social Engagement: Like posts (with duplicate-like prevention) and add/delete comments.

-Progress Analytics: Visual dashboard displaying total practice hours, weekly trends, skill distributions, and active streaks.
.


## Industry relevance 

This architecture mirrors real-world production systems used by EdTech platforms (Duolingo, Coursera), fitness tracking ecosystems (Strava), and professional creator networks by demonstrating centralized data persistence, scalable UGC storage, and elastic API compute design
## Cloud computing concepts 

-SaaS & PaaS: Delivered as software over the internet utilizing managed cloud database and auth platforms.

-Cloud Database & Object Storage: Decoupling relational metadata from heavy binary media assets.

-REST API & Client-Server Architecture: Decoupled React SPA communicating with a Python FastAPI backend.

-Security & Scalability: JWT/OAuth authentication, RBAC, input sanitization, TLS encryption, and environment-based secrets management.
## Architecture 

Client (React SPA) ──► REST API (FastAPI) ──┬──► Cloud Database (Firestore)
                                            └──► Cloud Object Storage (S3 / Bucket)
## Technology stack

-Frontend: React, Vite, JavaScript, HTML5, CSS3
-Backend: Python, FastAPI, Pydantic, Uvicorn
-Database & Auth: Firebase Firestore, Firebase Auth
-Cloud Storage: Firebase Storage / S3-compatible object storage
-Deployment: Vercel (Frontend), Render (Backend)

## User's profile 

Users manage unique profiles identified by UUIDs, storing metadata such as username, email, bio, and avatar URLs hosted in cloud object storage.
## Hobby&skill tracking 

Users organize pursuits into categories (BEGINNER, INTERMEDIATE, ADVANCED) with active, paused, or completed status flags.
## Practice tracking

Sessions record duration and notes, automatically incrementing total time spent and recalculating calendar streaks.
## Goals&milestones

Users establish goals with target values and deadlines. Milestones break large goals down into achievable increments. Progress is calculated as:
Progress %=min(100,(current_value/target_value)×100)


## Cloud database

Centralized NoSQL document store maintaining ACID-compliant transactional consistency across users, skills, sessions, and posts.

## Cloud object storage

Binary assets are stored in cloud buckets; database records maintain secure HTTPS reference URIs.
## Community sharing

Users publish milestone updates to a global feed enriched with author profiles, timestamps, and media attachments.
## Likes&comments

Structured relational mapping with unique compound constraints prevents duplicate likes and enforces authorization checks on deletions.
## Analytics

Aggregates time-series practice data into JSON payloads consumed by dashboard charting components.
## Rest APIs

 Standardized HTTP endpoints (GET, POST, PUT, DELETE) adhering to RESTful conventions with robust error handling and status codes.

## Folder structure 

Cloud-Hobby-Skills-Tracker/
├── backend/
│   ├── requirement.txt
│   ├── aap.py
│   ├── schemas.py
│   ├── analytics_servics.py
│   ├── main.py
│   └── test_main.py
│   
├── Frontend/
│  └── Src/app.jsx
│  
├── .env.example
├── .gitignore
└── README.md
## Installation 

Ensure Python 3.10+, Node.js (v18+), and Git are installed on your machine.
## Environment variable 

PORT=8000
FIREBASE_PROJECT_ID=hobby-tracker-cloud
## Cloud development 

-Frontend: Deploy the Vite React build to Vercel or Netlify.
-Backend: Deploy the FastAPI application to Render or Railway.
-Database & Storage: Connect managed Firebase Firestore and Firebase Storage instances.
## Testing 

cd backend
pytest -v

## Security 

Token-based authentication (Firebase Auth / JWT).
Strict MIME type and file size validation (≤5MB).
Parameterized database queries preventing injection attacks.


## Privacy 

User data isolation ensures private practice logs are restricted to their authenticated owners.
Full GDPR-compliant account and data deletion support.
## Scalability 

-Horizontal backend scaling is achieved by running stateless FastAPI container instances behind a managed load balancer.

-Feed scaling utilizes efficient indexing and pagination to handle growing user bases.


## Failure handeling 

Exponential backoff retry policies handle transient database connection failures.

Orphaned storage cleanup jobs purge unreferenced cloud storage assets if subsequent database transactions fail.
## Results

Successfully implemented a fully functional cloud-native hobby and skills tracking platform with robust authentication, cloud storage, real-time analytics, and social community features.
## Author

* **GitHub:** [nandiniveram2009](https://github.com)
* **LinkedIn:** [Nandini Verma](https://linkedin.com)



## Scalability 

-Horizontal backend scaling is achieved by running stateless FastAPI container instances behind a managed load balancer.

-Feed scaling utilizes efficient indexing and pagination to handle growing user bases.


## Folder structure 

Cloud-Hobby-Skills-Tracker/
├── backend/
│   ├── requirement.txt
│   ├── db_services.py
│   ├── skill.py
│   ├── practice.py
│   └── posts.py
│   
├── Frontend/
│   ├── firebase.js
│   └── app.jsx
│   
├── .env.example
├── .gitignore
└── README.md
## Environment variable 

PORT=8000
FIREBASE_PROJECT_ID=hobby-tracker-cloud
## Folder structure 

Cloud-Hobby-Skills-Tracker/
├── backend/
│   ├── requirement.txt
│   ├── db_services.py
│   ├── skill.py
│   ├── practice.py
│   └── posts.py
│   
├── Frontend/
│   ├── firebase.js
│   └── app.jsx
│   
├── .env.example
├── .gitignore
└── README.md
