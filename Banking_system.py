import random                       #used to generate random account number
import json                         #used as a mini database to store user account details
import getpass
try:                                #used to handle value error

    #prints the interface and asked for users option
    print("Welcome to Brainxix Bank")
    print("1. Create account \n2. Login")

    user = int(input("Enter your option: "))

    #this chunk of code is used to confirm users password and ensure the password is strong

    if user == 1:
        while True:
            user_name = input("Name: ")
            if user_name.isalpha():
                break
            else:
                print("Your account name can only be letters")

        while True:

            password1 = getpass.getpass("Password: ")
            password2 = getpass.getpass("Confirm Password: ")

            if password1 == password2:
                user_password = password1
            else:
                print("Sorry, passwords do not match")
                continue

            has_upper = False
            has_lower = False
            has_digit = False
            has_special = False

            for char in user_password:
                if char.isupper():
                    has_upper = True
                elif char.islower():
                    has_lower = True
                elif char.isdigit():
                    has_digit = True
                else:
                    has_special = True

            if len(user_password) < 8:
                print("Password length must be at least 8 characters")
            elif not has_upper:
                print("Password must contain an uppercase letter")
            elif not has_lower:
                print("Password must contain a lowercase letter")
            elif not has_digit:
                print("Password must contain a number")
            elif not has_special:
                print("Password must contain a special character")
            else:
                print("Password confirmed!✅ \nPassword accepted!")
                break

        # this code generates the account number automatically
        with open("Bank_acct_details.json","r") as file:
            accounts = json.load(file)
        while True:
            
            acct_number = random.randint(1000000000,9999999999)
            duplicate = False
            for account in accounts:

                if account["account_number"] == acct_number:
                    duplicate = True
                    break


            if duplicate == False:
                break
            
        bal = 0

        print("Your account number is:", acct_number)
        print(f"Balance: ₦{bal:,}")

        account_details = {
            "name": user_name,
            "password": user_password,
            "account_number": acct_number,
            "balance": bal,

            #stores transaction history

            "transactions": [
            ]
        }
        #open existing accounts instead of deleting previous accounts

        try:
            with open("Bank_acct_details.json","r") as file:
                accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            accounts = []

        #convert old single account into multiple account format

        if isinstance(accounts, dict):
            accounts = [accounts]

        #add new account to existing accounts

        accounts.append(account_details)

        #save all accounts again

        with open("Bank_acct_details.json","w") as file:
            json.dump(accounts,file,indent=4)
        print("Account created successfully!")
    elif user == 2:
        ask_acct_no = int(input("Enter your account number: "))
        with open("Bank_acct_details.json","r") as file:
            accounts = json.load(file)

        #convert old account format if available

        if isinstance(accounts, dict):
            accounts = [accounts]

        current_user = None

        #search through all accounts

        for account in accounts:
            if ask_acct_no == account["account_number"]:
                current_user = account
                break
        if current_user is None:

            print("Account number not found")
        else:
            ask_password = getpass.getpass("Enter your password: ")

            if ask_password == current_user["password"]:
                print("Login successful!")

                while True:
                    print(
                        f"\nWelcome {current_user['name']}\n"
                        "1. Check Balance\n"
                        "2. Deposit\n"
                        "3. Withdraw\n"
                        "4. Transfer\n"
                        "5. Account Summary\n"
                        "6. Logout"
                    )

                    user_choice = int(input("Choose option: "))
                                        # To check your account balance

                    if user_choice == 1:
                        print(f"Balance: ₦{current_user['balance']:,}")

                    # To deposit into your account and stores the amount in the Json file

                    elif user_choice == 2:
                        amount = int(input("Enter amount to deposit: "))
                        current_user["balance"] += amount

                        #save deposit history

                        current_user["transactions"].append(
                            f"Deposited ₦{amount:,}"
                        )
                        with open("Bank_acct_details.json","w") as file:
                            json.dump(accounts,file,indent=4)
                        print("Deposit successful!")
                        print(f"Balance: ₦{current_user['balance']:,}")

                    # to withdraw from your account and the balance is deducted from your previous balance

                    elif user_choice == 3:
                        withdraw_amount = int(input("Enter amount to withdraw: "))

                        if withdraw_amount <= current_user["balance"]:
                            current_user["balance"] -= withdraw_amount

                            #save withdrawal history

                            current_user["transactions"].append(
                                f"Withdrew ₦{withdraw_amount:,}"
                            )
                            with open("Bank_acct_details.json","w") as file:
                                json.dump(accounts,file,indent=4)
                            print("Withdrawal successful!")
                            print(f"Balance: ₦{current_user['balance']:,}")
                        else:
                            print("Insufficient funds")

                    # To make transfer

                    elif user_choice == 4:
                        receiver_account = int(input("Enter receiver account number: "))
                        receiver = None

                        #search for receiver account

                        for account in accounts:
                            if account["account_number"] == receiver_account:
                                receiver = account
                                break
                        if receiver is None:
                            print("Receiver account not found")
                        elif receiver == current_user:
                            print("You cannot transfer to yourself")
                        else:

                            transfer_amount = int(input("Enter amount to transfer: "))

                            if transfer_amount <= current_user["balance"]:

                                #subtract from sender

                                current_user["balance"] -= transfer_amount

                                #add to receiver

                                receiver["balance"] += transfer_amount

                                #save sender transfer history

                                current_user["transactions"].append(
                                    f"Transferred ₦{transfer_amount:,} to {receiver_account}"
                                )

                                #save receiver transfer history

                                receiver["transactions"].append(
                                    f"Received ₦{transfer_amount:,} from {current_user['account_number']}"
                                )

                                with open("Bank_acct_details.json","w") as file:
                                    json.dump(accounts,file,indent=4)

                                print("Transfer successful!")
                                print(f"Your balance: ₦{current_user['balance']:,}")
                            else:
                                print("Insufficient funds")

                    #to log out from the system

                    elif user_choice == 5:

                        #display transaction summary before logout

                        print("\n========== TRANSACTION SUMMARY ==========")
                        print(f"Account Name: {current_user['name']}")
                        print(f"Account Number: {current_user['account_number']}")
                        print("\nTransactions:")

                        for transaction in current_user["transactions"]:

                            print("-", transaction)

                        print(f"\nCurrent Balance: ₦{current_user['balance']:,}")
                        print("=========================================")
                    elif user_choice ==6:
                        print("Logged out successfully!")

                        break

                    else:

                        print("Invalid option")

            else:

                print("Incorrect password")

except ValueError:

    print("Please enter a number")