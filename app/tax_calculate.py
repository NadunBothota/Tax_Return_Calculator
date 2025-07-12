# Function to calculate income tax based on Australian tax brackets (as of current rates)
def calculate_tax(income):
    if income <= 18200:
        return 0.0  # Tax-free threshold
    elif income <= 45000:
        return 0.19 * (income - 18200)  # 19% for income between $18,201–$45,000
    elif income <= 120000:
        return 5092 + 0.325 * (income - 45000)  # 32.5% for $45,001–$120,000
    elif income <= 180000:
        return 29467 + 0.37 * (income - 120000)  # 37% for $120,001–$180,000
    else:
        return 51667 + 0.45 * (income - 180000)  # 45% for income above $180,000

# Function to calculate Medicare Levy (2% of total income)
def calculate_medicare_levy(income):
    return 0.02 * income

# Function to calculate Medicare Levy Surcharge (MLS) based on income and PHI status
def calculate_medicare_levy_surcharge(income, has_phic):
    if has_phic:
        return 0.0  # No surcharge if private health insurance (PHI) is held
    if income <= 90000:
        return 0.0  # No surcharge for income up to $90,000
    elif income <= 105000:
        return 0.01 * income  # 1% for income $90,001–$105,000
    elif income <= 140000:
        return 0.0125 * income  # 1.25% for $105,001–$140,000
    else:
        return 0.015 * income  # 1.5% for income above $140,000
