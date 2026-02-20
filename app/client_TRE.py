import Pyro5.api
from user_Authentication import login_user, register_user

def validate_record(income, withheld):
    return income >= 0 and 0 <= withheld <= income


# Collect multiple biweekly income records from the user
def collect_records():
    records = []
    
    # Ask how many records the user wants to enter (max 26 biweekly periods)
    count = int(input("How many biweekly records (1-26)? "))
    
    for i in range(count):
    
        income = float(input(f"Enter taxable income #{i + 1}: "))

        withheld = float(input(f"Enter tax withheld #{i + 1}: "))
 
        if not validate_record(income, withheld):
            print("Invalid record. Withheld tax cannot exceed income.")
            return None
        
        # Store valid record as a tuple (income, withheld)
        records.append((income, withheld))
    
    return records


def main():
    print("Welcome to PITRE - TRE Client\n")
    
    # Ask user whether to register or login
    choice = input("Do you want to Login or Register? ").strip()
    
    # If user chooses Register, call register function
    if choice == "Register":
        if not register_user():
            return
    
    # After registration (or if Login chosen), authenticate user
    if not login_user():
        return

    # Get remote server URIs for Pyro connection
    server1_uri = input("Enter Server 1 URI: ")
    server2_uri = input("Enter Server 2 URI: ")
    
    # Create proxy object to communicate with Server 1
    estimator = Pyro5.api.Proxy(server1_uri)
    
    # Set database server URI on Server 1
    estimator.set_db_uri(server2_uri)

    # Get user's Person ID
    person_id = input("Enter your 6-digit Person ID: ")
    
    # Check if user has TFN (Tax File Number)
    has_tfn = input("Do you have a TFN? (yes/no): ").strip().lower() == "yes"

    # If user has TFN
    if has_tfn:
        tfn = input("Enter your TFN: ").strip()
        
        # Ask about private health insurance cover
        phic = input("Do you have private health insurance? (yes/no): ").strip().lower() == "yes"
        
        # Estimate tax using TFN
        result = estimator.estimate_with_tfn(person_id, tfn, phic)

        # If TFN records are not found
        if "error" in result:
            print(f"\n{result['error']}")
            
            # Ask user if they want to add tax records
            add_data = input("Would you like to add your tax records now? (yes/no): ").strip().lower()
            
            if add_data == "yes":
                records = collect_records()
                
                if records:
                    # Add new records to the database
                    estimator.add_tfn_records(tfn, records)
                    
                    # Recalculate tax estimate
                    result = estimator.estimate_with_tfn(person_id, tfn, phic)
                else:
                    return
            else:
                return
    
    # If user does NOT have TFN
    else:
        records = collect_records()
        
        if records is None:
            return
        
        phic = input("Do you have private health insurance? (yes/no): ").strip().lower() == "yes"
        
        # Estimate tax without TFN using manually entered records
        result = estimator.estimate_no_tfn(person_id, records, phic)

    # Display final tax estimation result
    print("\n--- Tax Estimate Result ---")
    for key, value in result.items():
        print(f"{key}: {value}")


# Run the program
if __name__ == "__main__":
    main()
