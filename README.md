Expense Tracker API

A RESTful expense tracking API built with Flask, SQLAlchemy, and JWT authentication.
This API allows users to securely manage expenses, categorize them, and view monthly spending summaries.

Features

User authentication with JWT

Create, update, and delete expenses

Categorize expenses

Monthly expense summary analytics

PostgreSQL database

Deployed API

Tech Stack

Python

Flask

SQLAlchemy

Marshmallow

JWT Authentication

PostgreSQL

Render (deployment)

API Endpoints
Auth

POST /auth/register
POST /auth/login

Expenses

GET /expenses
POST /expenses
PUT /expenses/{id}
DELETE /expenses/{id}

Analytics

GET /expenses/summary/monthly?year=<YYYY>

Deployment

The API is deployed on Render.

Example request:

GET https://expense-tracker-api-b2qa.onrender.com/expenses
Example Response
FLASK_ENV=development

## Screenshots

### Create Expense

![Create Expense](docs/screenshots/create-expense.png)

---

### List Expenses

![List Expenses](docs/screenshots/list-expenses.png)

---

### Monthly Summary

![Monthly Summary](docs/screenshots/monthly-summary.png)


