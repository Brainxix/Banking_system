import random                       #used to generate random account number
import json                         #used as a mini to store user account details

try:                                 #used to handle value error

    #prints the interface and asked  for users option

    print("Welcome to Brainxix Bank")
    print("1. Create account \n2. Login")

    user = int(input("Enter your option: "))

    #this chunk of code is used to confirm users password and ensure the password is strong

    if user == 1:
        user_name = input("Name: ")

        while True:
            password1 = input("Password: ")
            password2 = input("Confirm Password: ")

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

                print("Password confirmed!✅ \nProceeding ... \nPassword accepted!")
                break

                    # this code generates the account number automatically and stores it in the Json file

        acct_number = random.randint(1000000000, 9999999999)
        print("Your account number is:", acct_number)

        bal = 0
        print(f"Balance: ₦{bal:,}")


        account_details = {
            "name": user_name,
            "password": user_password,
            "account_number": acct_number,
            "balance": bal
        }


        with open("Bank_acct_details.json", "w") as file:
            json.dump(account_details, file, indent=4)


        print("Account created successfully!")


            #from this part is the login page
            #the user is asked to input his account number which is then confirmed in the database
            #same is done for the password



    elif user == 2:

        ask_acct_no = int(input("Enter your account number: "))

        with open("Bank_acct_details.json", "r") as file:
            account_details = json.load(file)


        if ask_acct_no == account_details["account_number"]:

            ask_password = input("Enter your password: ")

            if ask_password == account_details["password"]:

                print("Login successful!")

                #this takes you into the login page

                while True:

                    print(
                        f"\nWelcome {account_details['name']}\n"
                        "1. Check Balance\n"
                        "2. Deposit\n"
                        "3. Withdraw\n"
                        "4. Logout"
                    )

                    user_choice = int(input("Choose option: "))

                        # To check your account balance

                    if user_choice == 1:

                        print(f"Balance: ₦{account_details['balance']:,}")

                         # To deposit into your account and stores the amount in the Json file

                    elif user_choice == 2:

                        amount = int(input("Enter amount to deposit: "))

                        account_details["balance"] += amount

                        with open("Bank_acct_details.json", "w") as file:
                            json.dump(account_details, file, indent=4)

                        print(f"Deposit successful!")
                        print(f"Balance: ₦{account_details['balance']:,}")

                         # to withdraw from your account and the balance is deducted from your previous balance 

                    elif user_choice == 3:

                        withdraw_amount = int(input("Enter amount to withdraw: "))

                                #this code ensures the money you want to withdraw is not more than your actual balance

                        if withdraw_amount <= account_details["balance"]:

                            account_details["balance"] -= withdraw_amount

                            with open("Bank_acct_details.json", "w") as file:
                                json.dump(account_details, file, indent=4)

                            print("Withdrawal successful!")
                            print(f"Balance: ₦{account_details['balance']:,}")

                        else:
                            print("Insufficient funds")


                        #to log out from the system 

                        
                    elif user_choice == 4:

                        print("Logged out successfully!")
                        break


                    else:
                        print("Invalid option")


            else:
                print("Incorrect password")


        else:
            print("Account number not found")


except ValueError:
    print("Please enter a number")