import os
import csv
from encryption import *
from datetime import date
from prettytable import from_csv
from prettytable import PrettyTable
from bullet import Password

details = "details.csv"
inv = "inventory.csv"
warning = "warning.csv"

def view_stat(sl):

	x = PrettyTable()
	x.field_names = ["SL.NO", "USER ID", "STATUS", "SECURITY DEPOSIT", "CREDIT", "SCORE", "FLEXIBILITY", "TRANSACTIONS"]

	csvr_file = csv.reader(open(details, "r"), delimiter=",")
	csvr_list = list(csvr_file)

	sln = int(sl)
	SLNO = csvr_list[sln][0]
	UID = csvr_list[sln][1]
	STS = csvr_list[sln][3]
	SEC = csvr_list[sln][4]
	CRD = csvr_list[sln][5]
	SCR = csvr_list[sln][6]
	FLEX = csvr_list[sln][7]
	TRANS = csvr_list[sln][8]

	if len(csvr_list) > 2:

		for i in range(len(csvr_list)):

			if i == (int(sl)):

				x.add_row([SLNO, UID, STS, SEC, CRD, SCR, FLEX, TRANS])

		print(x)

def add_crd(sl):

	amt = float(input("\n\tEnter the amount you want to add to credit: "))

	csv_file = csv.reader(open(details, "r"), delimiter=",")
	csvr = list(csv_file)

	os.remove(details)

	crd = float(csvr[sl][5])
	sec = float(csvr[sl][4])
	tran = int(csvr[sl][8])
	flex = float(csvr[sl][7])
	crd = crd + amt
	sec = crd*(1-flex)
	tran = tran + 1
	csvr[sl][5] = crd
	csvr[sl][4] = sec
	csvr[sl][8] = tran

	today = date.today()
	trans_details = csv.writer(open(f"Details/{csvr[sl][1]}.csv", "a+"),delimiter=",")
	trans_details.writerow([today,tran,f"{amt} has been added in your credit"])

	os.mknod(details)
	writer = csv.writer(open(details, "w"),delimiter=",")
	writer.writerows(csvr)

	print(f"\n\t{amt} has been added in your credit")
	print(f"\tNow you have {csvr[sl][5]} in your credit payment\n")


def buy(sl):

	csv_file = csv.reader(open(inv, "r"), delimiter=",")
	detail_file = csv.reader(open(details, "r"), delimiter=",")
	csvr_detail = list(detail_file)
	csvr = list(csv_file)
	for g in range(len(csvr_detail)):
		if csvr_detail[g][3] == "wholesaler":
			admin_sl = g

	with open(inv, "r") as fp:
		x = from_csv(fp)

	print(x)

	os.remove(details)
	os.remove(inv)

	nrow = len(csvr)
	cust_Bal = float(csvr_detail[sl][5])
	cust_sec = float(csvr_detail[sl][4])
	score = int(csvr_detail[sl][6])
	tran = int(csvr_detail[sl][8])
	flex = float(csvr_detail[sl][7])
	admin_bal = float(csvr_detail[admin_sl][5])
	admin_sec = float(csvr_detail[admin_sl][4])

	flag=1
	total = 0
	slno = []
	quan = []
	i = 0
	bought = False
	s_check = False
	q_check = False
	amt_check = False

	while flag == 1:

		add = input("Do You want to add medicine in basket(Y/N): ")

		if add == "Y" or add == "y":

			while s_check == False:

				s = int(input("\tEnter the Sl.no of the medicine you want to buy: "))

				if s < 1 or s >= nrow and s in slno:

					print("\t********Serial No. error********")

				else:

					s_check = True

			while q_check == False:

				q = int(input("\tEnter the quantity: "))
				qu = int(csvr[s][2])

				if q > qu or q < 0:

					print("\t********quantity error********")

				else:

					q_check = True

			slno.append(s)
			quan.append(q)
			price = float(csvr[slno[i]][3])
			nt_price = price*quan[i]
			total = total + nt_price
			i = i + 1

			s_check = False
			q_check = False

		else:
			flag=0
	if total != 0:

		print(f"\tYour total amount is {total}")
		print("\tHow do you want to pay?")
		print("\t1.Cash\n\t2.Credit\n\t3.Cancel")

		opt_check = 0

		while opt_check == 0:

			opt = int(input("\tPayment method: "))

			if opt != 1 and opt != 2 and opt != 3:

				print("********Option Error********")

			else:

				opt_check = 1

		if opt == 1:

			print("\tCash Transaction going on.......")
			admin_sec = admin_sec + total
			admin_bal = admin_bal + total
			bought = True

		elif opt == 2:

			print("\tCredit Transaction going on.......")

			if total <= (cust_Bal - cust_sec):

				cust_Bal = cust_Bal - total
				bought = True

			else:
				needed = (total-cust_Bal+(cust_Bal*(1-flex)))/flex
				print(f"\n\tYou need to add atleast {needed} in your credit to proceed")

				while amt_check == False:

					amt = float(input("\n\tEnter the amount you want to add to credit: "))

					if amt < (needed):

						print("\t********You Entered Wrong Amount********")

					else:

						amt_check = True

				cust_Bal = cust_Bal + amt
				cust_sec = cust_Bal * (1-flex)
				cust_Bal = cust_Bal - total
				
				bought = True

		else:

			bought = False
			print("\n\t********You didn't buy anything********\n")
			if score > 0:
				score = score - 1

	else:

		print("\n\t********You didn't buy anything********\n")
		if score > 0:
			score = score - 1

	if bought == True:

		print("\n\t********You have successfully purchased********\n")
		print(f"\tYour current credit is {cust_Bal}")
		print(f"\tYour current Security deposit is {cust_sec}\n")

		score = score + 1
		tran = tran + 1
		today = date.today()

		trans_details = csv.writer(open(f"Details/{csvr_detail[sl][1]}.csv", "a+"),delimiter=",")

		if opt == 1:

			trans_details.writerow([today,tran,f"You have purchased medicine of {total} using cash payment",])

		elif opt == 2:

			trans_details.writerow([today,tran,f"You have purchased {total} using credit payment",])


		for j in range(i):

			med = int(csvr[slno[j]][2])
			med = med - quan[j]
			csvr[slno[j]][2] = med

	csvr_detail[sl][5] = cust_Bal
	csvr_detail[sl][4] = cust_sec
	csvr_detail[sl][6] = score
	csvr_detail[sl][8] = tran
	csvr_detail[admin_sl][5] = admin_bal
	csvr_detail[admin_sl][4] = admin_sec

	os.mknod(details)
	os.mknod(inv)

	writer_details = csv.writer(open(details, "w"),delimiter=",")
	writer_details.writerows(csvr_detail)
	writer = csv.writer(open(inv, "w"),delimiter=",")
	writer.writerows(csvr)
	war = csv.writer(open(warning,"a+"),delimiter=",")

	if (cust_Bal - cust_sec) == 0:

		print("\t********You have exhausted your credit limit********")
		print("\t******A warning has been sent to the wholesaler*****")
		war.writerow([csvr_detail[sl][0],csvr_detail[sl][1],csvr_detail[sl][6],csvr_detail[sl][8],csvr_detail[sl][7]])

def hist(sl):

	csv_file = csv.reader(open(details, "r"), delimiter=",")
	csvr = list(csv_file)
	trans = int(csvr[sl][8])

	print("\n")

	if trans != 0:

		with open(f"Details/{csvr[sl][1]}.csv", "r") as trans_file:
			transr = from_csv(trans_file)

		print(transr)

	else:

		print("\t********No History********")

	print("\n")

def pass_change(sl):

	csv_file = csv.reader(open(details, "r"), delimiter=",")
	csvr = list(csv_file)

	cl_1 = Password(prompt="Enter the current password: ",hidden="*")
	cl_2 = Password(prompt="Enter the new password: ",hidden="*")

	pw1 = cl_1.launch()
	PWD1= encode(pw1)

	tran = int(csvr[sl][8])

	if PWD1 == csvr[sl][2]:

		os.remove(details)
		pw2 = cl_2.launch()
		PWD2 = encode(pw2)

		csvr[sl][2] = PWD2
		os.mknod(details)
		tran = tran + 1
		csvr[sl][8] = tran
		writer = csv.writer(open(details, "w"),delimiter=",")
		writer.writerows(csvr)

		print(f"\n\tPassword has been changed\n")

		today = date.today()
		trans_details = csv.writer(open(f"Details/{csvr[sl][1]}.csv", "a+"),delimiter=",")
		trans_details.writerow([today,tran,"Your password was changed"])

	else:

		print("********You entered wrong password********")




def user_fn(sl):

	flag = 0

	while flag == 0:

		print("\nChoose from the options:")
		print("1. View Status")
		print("2. Add Credit")
		print("3. Buy")
		print("4. History")
		print("5. Change Password")
		print("6. Log Out")
		choice = int(input("Enter Your choice: "))

		if choice == 1:

			view_stat(sl)

		elif choice == 2:

			add_crd(sl)

		elif choice == 3:

			buy(sl)

		elif choice == 4:

			hist(sl)

		elif choice == 5:

			pass_change(sl)

		elif choice == 6:

			print("\n\t********Logging Out********\n")
			flag = 1

		else:

			print("\n********Wrong Choice, Try again********")
