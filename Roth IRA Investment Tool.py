#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Function to calculate future value based on compound interest formula
def calculate_future_value(principal, rate, time):
    return principal * (1 + rate / 100) ** time

# Function to calculate how much to invest monthly to reach the goal
def calculate_investment_goal(age, retirement_age, current_value, target_value, annual_return_rate, monthly_contribution):
    years_to_invest = retirement_age - age
    if years_to_invest <= 0:
        return "Retirement age should be greater than current age!"
    
    # Future value from current investments
    future_value_factor = (1 + annual_return_rate / 100) ** years_to_invest
    future_value = current_value * future_value_factor
    
    # If current value meets or exceeds the target
    if future_value >= target_value:
        return "You're on track! You don't need to invest more."
    
    # Calculate monthly investment needed
    monthly_rate = annual_return_rate / 12 / 100
    months = years_to_invest * 12
    
    # Calculate the future value of current monthly contributions
    contribution_future_value = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    
    # Total future value including current value and contributions
    total_future_value = future_value + contribution_future_value
    
    if total_future_value >= target_value:
        return f"Your current contributions of ${monthly_contribution:.2f} are enough to reach your target."
    
    # If not enough, calculate additional monthly investment needed
    additional_investment_needed = (target_value - total_future_value) / (((1 + monthly_rate) ** months - 1) / monthly_rate)
    
    return max(round(additional_investment_needed, 2), 0)

# AI-based analysis to optimize contribution plan (Simple Linear Regression for this example)
def optimize_contributions(age, retirement_age, current_value, target_value, risk_level):
    # Sample data based on historical returns
    X = np.array([[25], [35], [45], [55], [65]])  # Sample ages
    y = np.array([7, 5, 3, 2, 1])  # Corresponding returns for risk levels (7%, 5%, 3% as example)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future return rate based on the user's age and risk level
    predicted_return = model.predict(np.array([[age]])).item()
    
    # Adjust return rate based on risk tolerance
    if risk_level == 'Low':
        predicted_return -= 1
    elif risk_level == 'High':
        predicted_return += 1
    
    return predicted_return

# Function to plot investment growth
def plot_investment_growth(current_value, annual_return_rate, years_to_invest, monthly_contribution):
    years = np.arange(0, years_to_invest + 1)
    future_values = [calculate_future_value(current_value + monthly_contribution * 12 * year, annual_return_rate, year) for year in years]

    plt.plot(years, future_values, marker='o', linestyle='-', color='b')
    plt.title("Investment Growth Over Time")
    plt.xlabel("Years")
    plt.ylabel("Investment Value ($)")
    plt.grid(True)
    plt.show()

# Function to save the result to a text file
def save_to_file(age, retirement_age, current_value, target_value, annual_return_rate, risk_level, result, monthly_contribution):
    filename = f"Roth_IRA_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write("----- Roth IRA Investment Summary -----\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("Investment Overview:\n")
        f.write(f" - Current Age: {age}\n")
        f.write(f" - Planned Retirement Age: {retirement_age}\n")
        f.write(f" - Time to Invest: {retirement_age - age} years\n\n")
        
        f.write("Financial Inputs:\n")
        f.write(f" - Current Investment Value: ${current_value:,.2f}\n")
        f.write(f" - Target Retirement Value: ${target_value:,.2f}\n")
        f.write(f" - Current Monthly Contribution: ${monthly_contribution:.2f}\n")
        f.write(f" - Expected Annual Return Rate (AI-Predicted): {annual_return_rate:.2f}%\n")
        f.write(f" - Risk Tolerance: {risk_level}\n\n")
        
        f.write("Analysis:\n")
        f.write(f" - Based on your inputs and current contributions, the system calculated:\n")
        f.write(f"   {result}\n\n")
        
        f.write("Recommendation:\n")
        if "on track" in result:
            f.write(" - No additional investments needed. Your current strategy is sufficient.\n")
        else:
            f.write(" - Consider increasing your monthly contributions to meet your retirement goal.\n")
            
        f.write("\nThank you for using the Roth IRA Tracker!\n")
    
    messagebox.showinfo("Saved", f"Analysis saved to {filename}")

# Function to handle button click
def calculate():
    try:
        age = int(age_entry.get())
        retirement_age = int(retirement_age_entry.get())
        current_value = float(current_value_entry.get())
        target_value = float(target_value_entry.get())
        monthly_contribution = float(contribution_entry.get())
        risk_level = risk_entry.get()
        
        # Validate risk level
        if risk_level not in ["Low", "Medium", "High"]:
            messagebox.showerror("Input Error", "Risk level must be Low, Medium, or High.")
            return
        
        # Predict the best annual return based on AI model
        annual_return_rate = optimize_contributions(age, retirement_age, current_value, target_value, risk_level)
        
        result = calculate_investment_goal(age, retirement_age, current_value, target_value, annual_return_rate, monthly_contribution)
        result_label.config(text=f"Result: {result}")
        
        # Save the result to a file
        save_to_file(age, retirement_age, current_value, target_value, annual_return_rate, risk_level, result, monthly_contribution)
        
        # Plot the investment growth over time
        plot_investment_growth(current_value, annual_return_rate, retirement_age - age, monthly_contribution)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Creating the UI
root = tk.Tk()
root.title("Roth IRA Tracker with AI")

# Labels and Entry fields for user input
tk.Label(root, text="Current Age:").grid(row=0, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=0, column=1)

tk.Label(root, text="Retirement Age:").grid(row=1, column=0)
retirement_age_entry = tk.Entry(root)
retirement_age_entry.grid(row=1, column=1)

tk.Label(root, text="Current Investment Value:").grid(row=2, column=0)
current_value_entry = tk.Entry(root)
current_value_entry.grid(row=2, column=1)

tk.Label(root, text="Target Retirement Value:").grid(row=3, column=0)
target_value_entry = tk.Entry(root)
target_value_entry.grid(row=3, column=1)

tk.Label(root, text="Monthly Contribution:").grid(row=4, column=0)
contribution_entry = tk.Entry(root)
contribution_entry.grid(row=4, column=1)

tk.Label(root, text="Risk Tolerance (Low, Medium, High):").grid(row=5, column=0)
risk_entry = tk.Entry(root)
risk_entry.grid(row=5, column=1)

# Button to trigger the calculation
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=6, column=0, columnspan=2)

# Label to display the result
result_label = tk.Label(root, text="Result: ")
result_label.grid(row=7, column=0, columnspan=2)

root.mainloop()



# In[ ]:





# In[ ]:




