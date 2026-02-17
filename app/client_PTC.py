import Pyro5.api
from user_Authentication import login_user, register_user

# Income must be positive (or zero)
# Withheld tax must not exceed income
def validate_record(income, withheld):
    return income >= 0 and 0 <= withheld <= income


def main():
    # Display system welcome message
    print("Welcome to PITRE - PTC Client\n")
    
    # Ask user whether to register or login
    choice = input("Do you want to Login or Register? ").strip()
    
    # If user selects Register, attempt registration first
    if choice == "Register":
        if not register_user():
            return  # Exit if registration fails
    
    # Authenticate user before proceeding
    if not login_user():
        return  # Exit if login fails

    # Get Server 2 URI for database connection
    server2_uri = input("Enter Server 2 URI: ")
    
    # Create Pyro proxy object to communicate with remote database server
    pitd = Pyro5.api.Proxy(server2_uri)

    # Get user's Tax File Number (TFN)
    tfn = input("Enter TFN: ").strip()
    
    # Ask how many tax records the user wants to add
    count = int(input("How many records do you want to add? (1–26): "))

    # Loop through the number of records entered
    for i in range(count):
        
        # Get gross income for the record
        income = float(input(f"Enter gross income #{i+1}: "))
        
        # Get tax withheld for the record
        withheld = float(input(f"Enter tax withheld #{i+1}: "))
        
        # Validate record before sending to server
        if not validate_record(income, withheld):
            print("Invalid record. Skipping.")
            continue  # Skip invalid records and continue loop
        
        # Send valid record to remote database server
        pitd.add_tax_record(tfn, income, withheld)
        
        print(f"Record #{i+1} added.")

    # Final confirmation message
    print("\nAll valid records submitted to the database.")


# Entry point of the program
if __name__ == "__main__":
    main()
