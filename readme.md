# Spending Tracker

## Introduction
The **Spending Tracker** is a web application that helps users monitor and manage their grocery expenses on instant delivery platforms like Zepto, Blinkit, and Instamart. It offers features like setting budgets, visualizing spending trends, and receiving personalized advice powered by AI to optimize spending habits.

---

## Features
- **Upload Invoices**: Upload invoices to automatically track expenses.
- **Set Budgets**: Set monthly spending limits and track remaining amounts.
- **Spending Graph**: Visualize daily spending for the last 7 days.
- **Analytics Graph**: Compare essential vs. non-essential spending.
- **AI Insights**: Get personalized advice on reducing expenses and managing budgets with OpenAI's LLM.
---

## Installation

### Prerequisites
1. Python
2. Django
3. OpenAI API key (for AI-powered insights)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/shasss447/Spending-Tracker.git
   cd spending-tracker
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
3. Apply database migrations:
   ```bash
   python manage.py migrate
4. Start the development server:
   ```bash
   python manage.py runserver

## Usage
1. Upload Invoices: Use the upload button to add spending data from invoices.
2. Set Budget: Define your monthly budget using the "Set Budget" button.
3. View Graphs: Click the respective buttons to see spending and analytics graphs.
4. Get Insights: Change `base_url`=*https://api.openai.com/v1/chat/completions* and enter your OpenAI API key in `api_key` in `tracker/utility/utils.py` to enable personalized advice.

## Project Architecture
- Frontend: Django templates with JavaScript for interactivity.
- Backend: Django for handling APIs and database operations.
- Database: SQLite
- AI Integration: OpenAI API for generating spending insights.