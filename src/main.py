import csv
import os.path
from user import *
from admin import *
from encryption import *
from os import system, name
from bullet import Password

filename = "details.csv"

cl = Password(prompt="Enter the password: ",hidden="*")

def clear_screen():

	if name == 'nt':

		_ = system('cls')

	else:

		_ = system('clear')

def sign_up():

	# Check if wholesaler account already exists
	flag = 0
	csv_file = csv.reader(open(filename, "r"), delimiter=",")
	csv_check = list(csv_file)
	sl = len(list(csv_check))

	for i in range(sl):

		if csv_check[i][3] == "wholesaler":

			flag = 1
			break

	while True:

		flag_1 = 0
		UID = input("Enter the User ID: ")

		for i in range(len(csv_check)):

			if csv_check[i][1] == UID:

				print("User ID already present! Please try again.")
				flag_1 = 1
				break

		if flag_1 == 0:

			break

	pw = cl.launch()
	PWD = encode(pw)

	# If wholesaler account exists, cannot create another wholesaler account
	if flag == 0:
		print("********ALERT********")
		print("This is the first account so it will be a wholesaler account.")
		chc = input("Do you want to proceed? (Y/N) ")

		if chc != "Y" and chc != "y":

			return

		STS = "wholesaler"
		CRD = float(input("Enter Wholesaler Balance: "))
		SEC = CRD
		FLEX = 0

	# If wholesaler account exists, cannot create another wholesaler account
	else:

		print("1. Retailer\n2. Distributor")
		chs_check = 0

		while chs_check == 0:

			choice = input("Enter your choice: ")

			if choice != "1" and choice != "2":

				print("********Wrong Choice********")

			else:

				crd_check = 0

				while crd_check == 0:

					CRD = float(input("Enter Credit amount in Rs: "))

					if CRD >= 2500:

						print("*******You Entered Wrong Amount********")
						print("********Must be less than 2500*********")

					else:

						crd_check = 1

				if choice == "1":

					STS = "retailer"

				else:

					STS = "distributor"

				SEC = float(CRD/2)
				FLEX = 0.5
				chs_check = 1
	SCR = 0
	TRAN = 0

	# Register a new user
	with open(filename, "a+") as csvfile:

		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([sl,UID,PWD,STS,SEC,CRD,SCR,FLEX,TRAN])

	if STS == "wholesaler":

		os.mknod(f"Details/{UID}.csv")
		trans_details = csv.writer(open(f"Details/{UID}.csv", "a+"),delimiter=",")
		trans_details.writerow(["DATE","SL.NO","TRANSACTION"])
		trans_details = csv.reader(open(f"Details/{UID}.csv", "a+"),delimiter=",")
		tran_len = len(list(trans_details))
		if tran_len >= 1:
			admin_fn(sl)

	elif STS == "retailer" or STS == "distributor":

		os.mknod(f"Details/{UID}.csv")
		trans_details = csv.writer(open(f"Details/{UID}.csv", "a+"),delimiter=",")
		trans_details.writerow(["DATE","SL.NO","TRANSACTION"])
		trans_details = csv.reader(open(f"Details/{UID}.csv", "a+"),delimiter=",")
		tran_len = len(list(trans_details))
		if tran_len >= 1:
			user_fn(sl)



def sign_in():

	flag = 0
	csv_file = csv.reader(open(filename, "r"), delimiter=",")
	UID = input("Enter the User ID. ")
	pw = cl.launch()
	PWD = encode(pw)
	csvr = list(csv_file)
	length = len(csvr)

	for i in range(length):

		if csvr[i][1] == UID:

			if csvr[i][2] == PWD:

				flag = 1
				STS = csvr[i][3]
				sl = int(csvr[i][0])
				break

			else:

				flag = 0.5

	if flag == 1:

		warn_details = csv.writer(open(f"warning.csv", "a+"),delimiter=",")

		if STS == "wholesaler":

			admin_fn(sl)

		elif STS == "retailer" or STS == "distributor":

			user_fn(sl)

	elif flag == 0.5:

		print("********Wrong password********")
		sign_in()

	else:

		print("User Not registered! Please register here: ")
		sign_up()

choice = "1"
while choice == "1" or choice == "2":

	clear_screen()
	path = "Details"
	isdir = os.path.isdir(path)

	if isdir == False:

		os.mkdir(path)

	print("**********************Welcome to Med-Ex**********************")
	print("1. Sign Up\n2. Sign In\nPress any other key to exit.")
	choice = input("Enter your choice: ")

	if choice == "1":

		sign_up()

	elif choice == "2":

		sign_in()

	else:

		print("********Thank You********")
		choice = "Something Else"
