from openai import OpenAI
PROMPT="""
You are a financial advisor designed to help users manage their expenditures based on their budget and spending patterns. Analyze the user's data, identify areas where they are overspending, and suggest actionable steps to bring their expenses within their budget. Prioritize essential items and recommend cost-cutting measures for non-essential or excessive spending. Example: A user has a budget of ₹10,000 but has spent ₹12,000 in the last 30 days. The spending includes groceries and junk items like chips, biscuits, and frozen food. Advise the user to prioritize essential groceries like rice, vegetables, and milk, and reduce or remove purchases of non-essential junk items such as chips and biscuits. For example:
    - Reduce spending on chips and biscuits from ₹2,000 to ₹500, saving ₹1,500.
    - Suggest buying frozen food only when necessary, reducing spending from ₹1,200 to ₹600, saving ₹600.
    - These adjustments will save the user ₹2,100, bringing their total expenditure down to ₹9,900, within the budget.
"""
from openai import OpenAI

def response(budget, total_spent, items):
    client = OpenAI(base_url="http://127.0.0.1:1234/v1/", api_key="your_api_key")
    content = (
        f"My current budget is ₹{budget}, and my total expenditure over the last 30 days "
        f"is ₹{total_spent}. Here are the details of my spending:\n"
        f"{', '.join([f'Item: {item[0]}, Quantity: {item[2]}, Price: ₹{item[1]}' for item in items])}\n\n"
        f"I want to reduce my expenditure to stay within my budget. Please provide advice "
        f"on how I can adjust my spending habits. Focus on identifying areas where I can cut "
        f"costs without compromising on essentials."
    )
    
    message = [
        {'role': 'system', 'content': PROMPT},
        {'role': 'user', 'content': content}
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=250
    )
    
    return response.choices[0].message.content


