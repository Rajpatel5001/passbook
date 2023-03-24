
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankinfo.settings')
#   title = models.CharField(max_length=1)
#     desciption = models.CharField(max_length=150)
#     number = models.IntegerField(default=0)
import django
django.setup()

from datetime import datetime
from faker import Faker
from passbook.models import passbookInfoModel
import random
from passbook.serilizer import passbookserilizer

fake = Faker()


def remin(data):
    try:
        balance = passbookInfoModel.objects.values('balance').last()['balance']
    except:
        balance = 0
        balance = balance - data["debit"] + data["credit"]
    return str(balance)


def populate(N=5):
    for _ in range(N):
        # fake_date = str(fake.date_between_dates(date_start=datetime(2023,3,20)),date_end=datetime(2023,3,20))
        fake_date = '2023-03-17'
        fake_particular = random.choice(["Telephone",
                                         "Travelling",
                                         "Office",
                                         "Supplies",
                                         "Utility Expenses",
                                         "Property Tax",
                                         "Legal Expenses",
                                         "Bank Charges",
                                         "Repair",
                                         "Insurance Expenses",
                                         "Advertising Expenses",
                                         "Research Expenses",
                                         "Entertainment Expenses",
                                         "Sales Expenses",
                                         "Product Cost",
                                         "Rental Cost",
                                         "Depreciation Expenses",
                                         "Others Costs"])
        
        fake_debit_credit = random.choice(["DEBIT", "CREDIT"])
        if fake_debit_credit == "DEBIT":

            fake_debit = int(fake.pydecimal(
            left_digits=8, right_digits=2, positive=True))
            fake_credit = 0
        else: 
            fake_credit = int(fake.pydecimal(
            left_digits=8, right_digits=2, positive=True))
            fake_debit = 0
        data = {
            "entry_created_date": fake_date,
            "particular": fake_particular,
            "debit": fake_debit,
            "credit":fake_credit
        }
        data["balance"] = remin(data)
        # entry
        serailizer = passbookserilizer(data=data)
        if serailizer.is_valid():
            serailizer.save()
        else:
            print(serailizer.errors)


if __name__ == '__main__':
    print("populate start")
    populate(10000)
    print("populatine complate")
