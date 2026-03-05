# Expense Tracker API

A RESTful expense tracking API built with **Flask**, **SQLAlchemy**, and **JWT authentication**.

This API allows users to securely manage their expenses, categorize spending, and generate monthly summaries.

---

# Features

- User authentication using **JWT**
- Create, update, and delete expenses
- Categorize expenses
- Monthly expense summary analytics
- PostgreSQL database
- Deployed REST API

---

# Tech Stack

- Python
- Flask
- SQLAlchemy
- Marshmallow
- JWT Authentication
- PostgreSQL
- Render (deployment)

---

# API Endpoints

## Auth

Register a new user

POST /auth/register

Login and receive a JWT token

POST /auth/login

---

## Expenses

Get all expenses

GET /expenses

Create a new expense

POST /expenses

Update an expense

PUT /expenses/{id}

Delete an expense

DELETE /expenses/{id}

---

## Analytics

Get monthly expense totals for a given year

GET /expenses/summary/monthly?year=<YYYY>

Example:

GET /expenses/summary/monthly?year=2026

---

# Deployment

The API is deployed on **Render**.

Base API URL:

https://expense-tracker-api-b2qa.onrender.com

Example request:

GET /expenses  
Authorization: Bearer <your_token>

---

# Example Response

```json
{
  "month": "2026-03",
  "total": 118.25
}
```

## Screenshots

### Create Expense
![Create Expense](docs/screenshots/create-expense.png)

---

### List Expenses
![List Expenses](docs/screenshots/list-expenses.png)

---

### Monthly Summary
![Monthly Summary](docs/screenshots/monthly-summary.png)
