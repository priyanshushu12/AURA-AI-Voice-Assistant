def calculate_emi(principal, annual_rate, tenure_years):
    # Convert annual interest rate to monthly and into decimal form
    monthly_rate = (annual_rate / 12) / 100
    
    # Convert tenure in years to months
    tenure_months = tenure_years * 12
    
    # EMI formula
    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    
    return round(emi, 2)

def calculate_emi_from_input():
    principal_amount = float(input("Enter the principal loan amount: "))
    annual_interest_rate = float(input("Enter the annual interest rate (in %): "))
    loan_tenure_years = int(input("Enter the loan tenure in years: "))

    # EMI calculation
    emi_amount = calculate_emi(principal_amount, annual_interest_rate, loan_tenure_years)
    print(f"The EMI for the loan is: ₹{emi_amount}")
    return f"The EMI for the loan is: ₹{emi_amount}"
