import os
import csv
from encryption import *
from datetime import date
from prettytable import from_csv
from bullet import Password

details = "details.csv"
inv = "inventory.csv"
warning = "warning.csv"

def view_bal(sl):

	csv_file = csv.reader(open(details, "r"), delimiter=",")
	csvr = list(csv_file)

	print(f"\n\tYour Balance is {csvr[sl][5]}\n")

def add_bal(sl):

	amt = float(input("\n\tEnter the amount you want to add to Balance: "))

	csv_file = csv.reader(open(details, "r"), delimiter=",")
	csvr = list(csv_file)

	os.remove(details)

	tran = int(csvr[sl][8])
	crd = float(csvr[sl][5])
	sec = float(csvr[sl][4])
	crd = crd + amt
	sec = crd
	tran = tran + 1
	csvr[sl][5] = crd
	csvr[sl][4] = sec

	today = date.today()
	trans_details = csv.writer(open(f"Details/{csvr[sl][1]}.csv", "a+"),delimiter=",")
	trans_details.writerow([today,tran,f"{amt} has been added in your Balance"])

	csvr[sl][8] = tran

	os.mknod(details)
	writer = csv.writer(open(details, "w"),delimiter=",")
	writer.writerows(csvr)

	print(f"\n\t{amt} has been added in your Balance\n")

def add_inv(sl):

	csv_file = csv.reader(open(inv, "r"), delimiter=",")
	detail_file = csv.reader(open(details, "r"), delimiter=",")
	csvr_detail = list(detail_file)
	csvr = list(csv_file)

	with open(inv, "r") as fp:
		x = from_csv(fp)

	print(x)
	os.remove(details)
	os.remove(inv)

	tran = int(csvr_detail[sl][8])
	nrow = len(csvr)
	admin_bal = float(csvr_detail[sl][5])

	flag=1
	total = 0
	slno = []
	name = []
	q_old = []
	q_new = []
	p = []
	i = 0
	j = 0
	bought = False
	s_check = False
	q_check = False
	amt_check = False

	while flag == 1:

		add = input("Do You want to add medicine in Inventory(Y/N): ")

		if add == "Y" or add == "y":

			print("\tWhat kind of medicine you want to add?\n	1.New\n	2.Old")
			typ = int(input("\tEnter Your choice: "))

			if typ == 1:

				name.append(input("\tEnter the medicine name: "))
				q_new.append(int(input("\tEnter the quantity: ")))
				p.append(int(input("\tEnter the price per medicine: ")))
				price_new = p[i]*q_new[i]
				total = total + price_new
				i = i + 1

			else:

				if typ != 2:

					print("\t********You have entered wrong input********")
					print("\t***********Taking *Old* as input************")

				while s_check == False:

					s = int(input("\tEnter the Sl.no of the medicine you want to buy: "))

					if s < 1 or s >= nrow and s in slno:

						print("\t********Serial No. error********")

					else:

						s_check = True

				while q_check == False:

					q = int(input("\tEnter the quantity: "))

					if q < 0:

						print("\t********quantity error********")

					else:

						q_check = True

				slno.append(s)
				q_old.append(q)
				price = float(csvr[slno[j]][3])
				price_old = price*q_old[j]
				total = total + price_old
				j = j + 1

				s_check = False
				q_check = False

		else:

			flag=0

	if total != 0:

		print(f"\tYour total amount is {total}")
		print("\tHow do you want to pay?")
		print("\t1.Cash\n\t2.Balance\n\t3.Cancel")

		opt_check = 0

		while opt_check == 0:

			opt = int(input("\tPayment method: "))

			if opt != 1 and opt != 2 and opt != 3:

				print("********Option Error********")

			else:

				opt_check = 1

		if opt == 1:

			print("\tCash Transaction going on.......")
			bought = True

		elif opt == 2:

			print("\tBalance Transaction going on.......")

			if total < admin_bal:

				admin_bal = admin_bal - total
				bought = True

			else:

				print("\n\tYou need to add Balance")

				while amt_check == False:

					amt = float(input("\n\tEnter the amount you want to add to Balance: "))

					if amt < (total - admin_bal):

						print("\t********You Entered Wrong Amount********")

					else:

						amt_check = True

				admin_bal = admin_bal + amt
				admin_bal = admin_bal - total
				bought = True

		else:

			bought = False
			print("\n\t********You didn't add anything********\n")

	else:

		print("\n\t********You didn't add anything********\n")

	csvr_detail[sl][5] = admin_bal
	csvr_detail[sl][4] = admin_bal

	if bought == True:

		print("\n\t********You have successfully added********\n")
		print(f"\tYour current Balance is {csvr_detail[sl][4]}\n")

		tran = tran + 1
		today = date.today()

		trans_details = csv.writer(open(f"Details/{csvr_detail[sl][1]}.csv", "a+"),delimiter=",")

		if opt == 1:

			trans_details.writerow([today,tran,f"You have purchased medicine of {total} using cash payment",])

		elif opt == 2:

			trans_details.writerow([today,tran,f"You have purchased medicine of {total} using Balance",])

		for k in range(j):

			med = int(csvr[slno[k]][2])
			med = med + q_old[k]
			csvr[slno[k]][2] = med

	os.mknod(details)
	os.mknod(inv)
	csvr_detail[sl][8] = tran
	writer_details = csv.writer(open(details, "w"),delimiter=",")
	writer_details.writerows(csvr_detail)
	writer = csv.writer(open(inv, "w"),delimiter=",")
	writer.writerows(csvr)

	writer_new = csv.writer(open(inv, "a+"))
	for t in range(i):
		writer.writerow([nrow+t,name[t],q_new[t],p[t]])

def user_details(sl):

	with open(details, "r") as csv_detail:
		csvr = from_csv(csv_detail)

	csvr_file = csv.reader(open(details, "r"), delimiter=",")
	csvr_list = list(csvr_file)

	if len(csvr_list) > 2:

		csvr.del_row(0)
		print(csvr.get_string(fields=["SL.NO", "USER ID", "STATUS", "SCORE", "FLEXIBILITY", "TRANSACTIONS"]))

	else:

		print("\n\t********No User Exists********")

def warning(sl):

	file = csv.reader(open("warning.csv", "r"), delimiter=",")
	csvr_file = csv.reader(open(details, "r"), delimiter=",")
	war = list(file)
	csvr = list(csvr_file)

	change = 0
	no_row = len(war)
	print("\n")

	if no_row <= 1:

		print("\tThere is no Notification")

	else:

		print("\tThe users whose credits have been exhausted are as follows:")

		with open("warning.csv", "r") as warn:
			x = from_csv(warn)

		print(x)

		os.remove("warning.csv")

		flag = 1
		s_check = False
		q_check = False

		while flag == 1:

			add = input("Do You want to change the flexibility of a user?(Y/N): ")

			if add == "Y" or add == "y":

				s = int(input("\tEnter the Sl.no of the user you want to change: "))

				while q_check == False:

					q = float(input("\tEnter the changed flexibility: "))

					if q < 0:

						print("	********flexibility error********")

					else:

						q_check = True

				csvr[s][7] = q

				s_check = False
				q_check = False

				os.remove(details)

				tran_admin = int(csvr[sl][8])
				tran_cust = int(csvr[s][8])

				tran_admin = tran_admin + 1
				tran_cust = tran_cust + 1

				today = date.today()
				trans_details = csv.writer(open(f"Details/{csvr[sl][1]}.csv", "a+"),delimiter=",")
				trans_details.writerow([today,tran_admin,f"You changed the flexibility of {csvr[s][1]}"])
				cust_trans = csv.writer(open(f"Details/{csvr[s][1]}.csv", "a+"),delimiter=",")
				cust_trans.writerow([today,tran_cust,f"Your flexibility has been changed by the wholesaler"])

				csvr[sl][8] = tran_admin
				csvr[s][8] = tran_cust

				os.mknod(details)
				writer_details = csv.writer(open(details, "w"),delimiter=",")
				writer_details.writerows(csvr)

			else:

				flag = 0



	if no_row > 1:
		os.mknod("warning.csv")
		writer_warn = csv.writer(open("warning.csv", "w"),delimiter=",")
		writer_warn.writerow(["SL.NO","USER ID","SCORE","TRANSACTION","FLEXIBILITY"])
		print("\n\t********All Notifications have been removed********")

	print("\n")

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

def admin_fn(sl):

	flag = 0

	while flag == 0:

		print("\nChoose from the options:")
		print("1. View Balance")
		print("2. Add Balance")
		print("3. Inventory")
		print("4. User details")
		print("5. Notifications")
		print("6. History")
		print("7. Change Password")
		print("8. Log Out")
		choice = int(input("Enter Your choice: "))

		if choice == 1:

			view_bal(sl)

		elif choice == 2:

			add_bal(sl)

		elif choice == 3:

			add_inv(sl)

		elif choice == 4:

			user_details(sl)

		elif choice == 5:

			warning(sl)

		elif choice == 6:

			hist(sl)

		elif choice == 7:

			pass_change(sl)

		elif choice == 8:

			print("\n\t********Logging Out********\n")
			flag = 1

		else:

			print("\n********Wrong Choice, Try again********")
