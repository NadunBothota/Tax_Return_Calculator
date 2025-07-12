import Pyro5.api
from user_Authentication import login_user, register_user

def validate_record(income, withheld):
    return income >= 0 and 0 <= withheld <= income

def collect_records():
    records = []
    count = int(input("How many biweekly records (1-26)? "))
    for i in range(count):
        income = float(input(f"Enter taxable income #{i + 1}: "))
        withheld = float(input(f"Enter tax withheld #{i + 1}: "))
        if not validate_record(income, withheld):
            print("Invalid record. Withheld tax cannot exceed income.")
            return None
        records.append((income, withheld))
    return records

def main():
    print("Welcome to PITRE - TRE Client\n")
    choice = input("Do you want to Login or Register? ").strip()
    if choice == "Register":
        if not register_user():
            return
    if not login_user():
        return

    server1_uri = input("Enter Server 1 URI: ")
    server2_uri = input("Enter Server 2 URI: ")
    estimator = Pyro5.api.Proxy(server1_uri)
    estimator.set_db_uri(server2_uri)
    person_id = input("Enter your 6-digit Person ID: ")
    has_tfn = input("Do you have a TFN? (yes/no): ").strip().lower() == "yes"

    if has_tfn:
        tfn = input("Enter your TFN: ").strip()
        phic = input("Do you have private health insurance? (yes/no): ").strip().lower() == "yes"
        result = estimator.estimate_with_tfn(person_id, tfn, phic)
        if "error" in result:
            print(f"\n{result['error']}")
            add_data = input("Would you like to add your tax records now? (yes/no): ").strip().lower()
            if add_data == "yes":
                records = collect_records()
                if records:
                    estimator.add_tfn_records(tfn, records)
                    result = estimator.estimate_with_tfn(person_id, tfn, phic)
                else:
                    return
            else:
                return
    else:
        records = collect_records()
        if records is None:
            return
        phic = input("Do you have private health insurance? (yes/no): ").strip().lower() == "yes"
        result = estimator.estimate_no_tfn(person_id, records, phic)

    print("\n--- Tax Estimate Result ---")
    for key, value in result.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
