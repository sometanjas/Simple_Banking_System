# Write your code here
import random
import sqlite3

# sqlite3jdbc:sqlite:/Users/vitaly/IdeaProjects/Simple Banking System/Simple Banking System/task/banking/card.s3db
# jdbc:sqlite:/Users/vitaly/IdeaProjects/Simple Banking System/Simple Banking System/task/card.s3db

con = sqlite3.connect('card.s3db')
cursor = con.cursor()
# cursor.execute("DROP TABLE card;")
# con.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS card(
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0);""")

# cursor.execute("INSERT INTO card VALUES (?,?)", card_pin_dict)


con.commit()
# cursor.close()
# con.close()


def menu():
    print("1. Create an account\n2. Log into account\n0. Exit")
    return int(input())


def main():
    card_pin_dict = {}  # card_num: pin
    while True:
        answer = menu()
        if answer == 1:
            checksum = 0
            print("Your card has been created\nYour card number: ")
            
            account_id = str(random.randint(100000000, 999999999))
            account_id_4 = '400000' + account_id
            # account_id_4 = "400000665055484"
            stringnumbers = list(account_id_4)
            numbers_int_list = [int(i) for i in stringnumbers]
            for i in range(0, len(numbers_int_list), 1):
                if i == 0 or i % 2 == 0:
                    numbers_int_list[i] = numbers_int_list[i] * 2
            for i in range(len(numbers_int_list)):
                if numbers_int_list[i] > 9:
                    numbers_int_list[i] = numbers_int_list[i] - 9
            # print(numbers_int_list)
            sum_number = sum(numbers_int_list)
            # print(sum_number)
            if sum_number % 10 != 0:
                checksum = 10 - (sum_number % 10)
                checksum = str(checksum)
            else:
                checksum = "0"
            # print(checksum)
            card_num = account_id_4 + checksum  # checksum
            print(card_num)
            print("Your card PIN: ")
            pin = str(random.randint(0, 9999)).rjust(4, '0')
            print(pin)
            card_pin_dict[card_num] = pin
            cursor.execute("INSERT INTO card(number, pin) VALUES (?,?)", (card_num, pin))
            con.commit()
        if answer == 2:
            print("Enter your card number: ")
            card_num_input = input()
            print("Enter your PIN: ")
            pin_input = input()
            # exist_card = card_num_input in card_pin_dict
            # exist_pin = pin_input == card_pin_dict.get(card_num_input)
            # if exist_card is True and exist_pin is True:
            cursor.execute("SELECT number, pin FROM card WHERE number = (?) AND pin = (?)", (card_num_input, pin_input))
            existing_entry = cursor.fetchone()
            if existing_entry is not None:
                print("You have successfully logged in!")
                handle_account(card_num_input)

            # if card_num_input in card_pin_dict and pin_input == card_pin_dict.get(card_num_input):
            #     print("You have successfully logged in!")
            #     interface_acc()
            if existing_entry is None:
                print("Wrong card number or PIN!")
                main()
            # menu()
        if answer == 0:
            print("Bye!")
            exit()


# def menu_acc():
#     print("1. Balance\n2. Log out\n0. Exit")
#     return int(input())
#
#
# def interface_acc():
#     answer = menu_acc()
#     if answer == 1:
#         print("Balance: 0")
#         interface_acc()
#     if answer == 2:
#         print("You have successfully logged out!")
#         menu()
#     if answer == 0:
#         print("Bye!")
#         exit()


def display_account_menu():
    print("1. Balance\n"
          "2. Add income\n"
          "3. Do transfer\n"
          "4. Close account\n"
          "5. Log out\n"
          "0. Exit")
    return int(input())


def handle_account(account):
    while True:
        answer = display_account_menu()
        if answer == 1:
            handle_account_balance(account)
        if answer == 2:
            handle_add_income(account)
        if answer == 3:
            handle_do_transfer(account)
        if answer == 4:
            close(account)
        if answer == 5:
            print("You have successfully logged out!")
            break
        if answer == 0:
            print("Bye!")
            exit()


def handle_account_balance(account):
    cursor.execute("SELECT balance FROM card WHERE number = (?)", (account,))
    balance = cursor.fetchone()
    print("Balance: ", balance)
    handle_account(account)


def handle_add_income(account):
    print("Enter income: ")
    income_str = input()
    income = int(income_str)
    cursor.execute("UPDATE card SET balance = balance + (?) WHERE number = (?)", (income, account))  #TODO
    con.commit()
    print("Income was added!")
    # handle_account(account)


def handle_do_transfer(account):
    print("Transfer\n"
          "Enter card number:")
    transfer_num = input()
    if account == transfer_num:
        print("You can't transfer money to the same account!")
    is_valid = true_num(transfer_num)
    if is_valid is True:
        print("Enter how much money you want to transfer:")
        transfer_money = int(input())
        handle_transfer(account, transfer_num, transfer_money)


def true_num(account):
    wo_checksum = account[:-1]
    wo_checksum_list = list(wo_checksum)
    numbers_int_list = [int(i) for i in wo_checksum_list]
    for i in range(0, len(numbers_int_list), 1):
        if i == 0 or i % 2 == 0:
            numbers_int_list[i] = numbers_int_list[i] * 2
    for i in range(len(numbers_int_list)):
        if numbers_int_list[i] > 9:
            numbers_int_list[i] = numbers_int_list[i] - 9
    sum_number = sum(numbers_int_list)
    if sum_number % 10 != 0:
        checksum = 10 - (sum_number % 10)
        checksum = str(checksum)
    else:
        checksum = str(checksum)
    card_num = wo_checksum + checksum  # checksum
    if card_num != account:
        print("Probably you made a mistake in the card number. Please try again!")
        return False
    cursor.execute("SELECT number FROM card WHERE number = (?)", (account,))
    is_valid = cursor.fetchone()
    if is_valid is None:
        print("Such a card does not exist.")
    return True


def handle_transfer(account, transfer_num, transfer_money):
    cursor.execute("SELECT balance FROM card WHERE number = (?)", (account,))
    current_balance = cursor.fetchone()
    if transfer_money <= current_balance[0]:
        cursor.execute("UPDATE card SET balance = balance - (?) WHERE number = (?)", (transfer_money, account))
        cursor.execute("UPDATE card SET balance = balance + (?) WHERE number = (?)", (transfer_money, transfer_num))
        con.commit()
        print("Success!")
    if transfer_money >= current_balance[0]:
        print("Not enough money!")


def close(account):
    cursor.execute("DELETE from card where number = (?)", (account,))
    con.commit()
    print("The account has been closed!")


main()
