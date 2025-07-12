import Pyro5.api
from user_Authentication import login_user, register_user

def validate_record(income, withheld):
    return income >= 0 and 0 <= withheld <= income

def main():
    print("Welcome to PITRE - PTC Client\n")
    choice = input("Do you want to Login or Register? ").strip()
    if choice == "Register":
        if not register_user():
            return
    if not login_user():
        return

    server2_uri = input("Enter Server 2 URI: ")
    pitd = Pyro5.api.Proxy(server2_uri)
    tfn = input("Enter TFN: ").strip()
    count = int(input("How many records do you want to add? (1–26): "))

    for i in range(count):
        income = float(input(f"Enter gross income #{i+1}: "))
        withheld = float(input(f"Enter tax withheld #{i+1}: "))
        if not validate_record(income, withheld):
            print("Invalid record. Skipping.")
            continue
        pitd.add_tax_record(tfn, income, withheld)
        print(f"Record #{i+1} added.")

    print("\nAll valid records submitted to the database.")

if __name__ == "__main__":
    main()
