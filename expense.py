import csv

def add_expense(date, item, amount):
    with open("expenses.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, item, amount])

def read_expenses():
    with open("expenses.csv", mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

add_expense("2025-06-18", "Groceries", 200)
read_expenses()
