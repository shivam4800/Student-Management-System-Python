from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext


import matplotlib.pyplot as plt
import numpy as np 

import requests 
import socket 
import bs4
import re
import datetime 

import webbrowser


from sqlite3 import *


root = Tk()
root.title("S.M.S")

root.geometry("500x610+250+250")
root.configure(background = 'SkyBlue1')
res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
#print(res)
soup = bs4.BeautifulSoup(res.text, 'lxml')
quote = soup.find('img', {"class":"p-qotd"})
#print(quote)
msg = quote['alt']
#print(msg)

d_date = datetime.datetime.now()
reg_date = d_date.strftime("%d/%m/%Y")
#print(reg_date)

try:
	socket.create_connection(("www.google.com",80))
	#print("you are connected")
	res = requests.get("https://ipinfo.io")
	#print(res)
	data = res.json()
	#print(data)
	city = data['city']
	#print(city)

	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address = a1 + a2 + a3
	res1 = requests.get(api_address)
	print(res1)
	data = res1.json()
	#print(data)
	
	atemp = data['main']['temp']
	#print("city ",city,"temp ",atemp)      

except Exception as e:
	print("Check connection",e)
def f1():
	root.withdraw()
	adst.deiconify()
def f2():
	adst.withdraw()
	root.deiconify()
def f3():  #View
	stdata.delete(1.0,END)
	root.withdraw()
	vist.deiconify()
	
	con = None
	try:
		con = connect('test.db')
		cursor = con.cursor()
		#sql = "select rno,name,marks from student"
		sql = "select * from student1 order by rno"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg = ""
		for d in data:
			msg = msg + "Roll no = " + str(d[0]) + " " + "Name = " + str(d[1]) + " " + "Marks = " + str(d[2]) + "\n"
		stdata.insert(INSERT, msg)
	except Exception as e:
		print("Issue",e)
	finally:
		if con is not None:
			con.close()             
def f4():
	vist.withdraw()
	root.deiconify()
def f5():
	root.withdraw()
	upst.deiconify()
def f6():
	upst.withdraw()
	root.deiconify()
def f7():
	root.withdraw()
	dlst.deiconify()
def f8():
	dlst.withdraw()
	root.deiconify()

def delete_add():
	entAddRno.delete(0,END)
	entAddName.delete(0,END)
	entAddMarks.delete(0,END)
	entAddRno.focus()

def delete_update():
	entUpdateRno.delete(0,END)
	#entUpdateName.delete(0,END)
	entUpdateMarks.delete(0,END)
	entUpdateRno.focus()
def f9():             #add student record
	
	con = None
	try:
		entAddRno.focus()  
		con = connect('test.db')
		rno = int(entAddRno.get())
		rno1=entAddRno.get()
		name = entAddName.get()
		marks = int(entAddMarks.get())
		
		if len(name) < 2:  
			
			messagebox.showerror("Issue", "Name cannot be less than 2 characters" )
			delete_add()
		
		
		elif name.isalpha()==False:
			
			messagebox.showerror("Issue", "Name cannot include digits or special characters")
			delete_add()
		elif marks < 0 or marks > 100:
			
			messagebox.showerror("Issue", "Marks cannot be less than 0 or greater than 100")
			delete_add()
		

		elif rno <= 0:
			
			messagebox.showerror("Issue","Roll Number cannot be zero or negative")
			delete_add()
		elif len(rno1) == 0:
			
			messagebox.showerror("Issue","Roll number cannot be empty! Please dont keep any fields empty!")
			delete_add()
		
		else:
			cursor = con.cursor()
			sql = "insert into student1 values('%d','%s','%d')"
			args = (rno,name,marks)
			cursor.execute(sql % args)
			con.commit()
			
			messagebox.showinfo("Success","Record added")
			delete_add()
	except ValueError as i: #error 
		
		messagebox.showerror("Issue","Invalid parameters")
		delete_add()
	except TypeError as e:  #error 
		
		messagebox.showerror("Issue","Invalid parameters")
		delete_add()
	except Exception as e:
		con.rollback() 
		delete_add()
		
		messagebox.showerror("Issue", e)
	finally:
		if con is not None:
			con.close()     

def f10():            #update student record 
	
	con = None
	try:
		con = connect('test.db')
		rno = int(entUpdateRno.get())
		#name = entUpdateName.get()
		marks = int(entUpdateMarks.get())
		'''if  len(name) < 2:
	
			messagebox.showerror("Issue", "Name cannot be less than 2 characters" )
			delete_update()
		#elif name.isalpha()==False :
			
		#messagebox.showerror("Issue", "Name cannot include digits or special characters")
			#delete_update()'''
		if marks < 0 or marks > 100:
			messagebox.showerror("Issue", "Marks cannot be less than 0 or greater than 100")
			delete_update()
		elif rno <= 0:
			messagebox.showerror("Issue", "Roll Number cannot be less than 0 or greater than 100")
			delete_update()
			
		else:
			cursor = con.cursor()
			sql = "select rno from student1 where rno = " +str(rno) 
			cursor.execute(sql)
			data = cursor.fetchall()
			if data:
				sql = "update student1 set marks = '%d' where rno = '%d'"
				args = (marks,rno)
				cursor.execute(sql % args)
				con.commit()

				messagebox.showinfo("Success","Record updated")
			else:
		
				messagebox.showerror("Issue","Record dosent exist")
		delete_update()
			
	except DatabaseError as e:
		con.rollback()
		print("issue",e)
		delete_update()
	except ValueError as i: #error 
		
		messagebox.showerror("Issue","Enter valid parameters")
		delete_update()
	except TypeError as e:  #error 
		
		messagebox.showerror("Issue","Enter valid parameters")
		delete_update()
	finally:
		if con is not None:
			con.close()

def f11():            #delete student record 
	con = None
	try:
		con = connect('test.db')
		cursor = con.cursor()
		rno  = int(entDeleteRno.get())
		sql = "select rno from student1 where rno = " +str(rno)  
		cursor.execute(sql)
		data = cursor.fetchall()
		if data:
			sql = "delete from student1 where rno = '%d'"
			args = (rno)
			cursor.execute(sql % args)
			con.commit()
			
			messagebox.showinfo("Succes","Record Deleted")
			entDeleteRno.delete(0,END)
			entDeleteRno.focus()
		else:
		
			messagebox.showerror("Issue","Record does not exist")
			entDeleteRno.delete(0,END)
			entDeleteRno.focus()
	
	except NameError as e:

		messagebox.showerror("Issue","Enter valid parameters")
		entDeleteRno.delete(0,END)
	except ValueError as e:
	
		messagebox.showerror("Issue","Enter valid parameters")
		entDeleteRno.delete(0,END)
	finally:
		if con is not None:
			con.close() 
def f12():  
	
	students = []
	highest = []
	marks = []
	rno=[]
	c = {}

	con = connect('test.db')
	cursor = con.cursor()
	sql = "select rno, name, marks from student1"
	cursor.execute(sql)
	fetch = cursor.fetchall()
	print(fetch)
	for d in fetch:
			mar = float(d[2])
			print(mar)
			marks.append(mar)
			stu = (d[1])
			print(stu)
			students.append(stu)
			rn=int(d[0])
			print(rn)
			rno.append(rn)
	
	
	print("Marks-",marks)
	print("Stu-",students)
	print("rno-",rno)
	d = dict(zip(rno,marks))
	r=dict(zip(rno,students))
	print("dict1: ",d)
	print("dict2: ",r)
	 
	
	L = list(d.items())
	print(L)
	L1=sorted(d.items(), key=lambda x: x[1])
	print("sort: ",L1)
	#print(lol)
	#b = L[-1:-6:-1]
	#print(b)
	a=L1[-1:-6:-1]
	print("sorted: ",a)
	
	c.update(a)
	na=[]
	check=[]
	check=list(c.keys())
	print("check: ",check)
	for c1 in check:

		na1=r[c1]
		print(na1)
		na.append(na1)
		
	print(c.values())
	print(c.keys())
	print(na)
	na2=list(range(len(na)))
	plt.bar(na2,c.values(), color = ['r','b','y','g','c'], width = 0.4)
	plt.title("TOP 5", fontsize = 27)
	plt.ylabel("Marks", fontsize = 13)
	plt.xlabel("Students", fontsize = 13)
	plt.xticks(na2, na)
	plt.grid()
	plt.show()
	con.close()








btnAdd = Button(root, text = "Add", font = ('arial',16,'bold'), width = 10, height = 1, command = f1)
btnView = Button(root, text = "View", font = ('arial',16,'bold'), width = 10, height = 1, command = f3)
btnUpdate = Button(root, text = "Update", font = ('arial',16,'bold'), width = 10, height = 1, command = f5)
btnDelete = Button(root, text = "Delete", font = ('arial',16,'bold'), width = 10, height = 1, command = f7)
btnGraph = Button(root, text = "Graph", font = ('arial',16,'bold'), width = 10, height = 1, command = f12)
lblCity = Label(root, text = "City:", font = ('arial',10,'bold'), width = 5,bg='SkyBlue1')
lblTemp = Label(root, text = "Temperature:", font = ('arial',10,'bold'), width = 10,bg='SkyBlue1')
lblQotd = Label(root, text = "Quote of the day:", font = ('arial',8,'bold'), width = 13,bg='SkyBlue1')
lblCityName = Label(root, text = city, font = ('arial',10,'italic'), width = 10,bg='SkyBlue1' )
lblCityTemp = Label(root, text = atemp, font = ('arial',10,'italic'), width = 5,bg='SkyBlue1')
lblQotdDaily = Label(root, text = msg, font = ('arial',8,'italic'),bg='SkyBlue1')
lblDate = Label(root, text = reg_date, font = ('arial',10,'italic'), width = 10,bg='SkyBlue')

btnAdd.place(x = 180, y = 20)
btnView.place(x = 180, y = 110)
btnUpdate.place(x = 180, y = 200)
btnDelete.place(x = 180, y = 290)
btnGraph.place(x = 180, y = 380)
lblCity.place(x = 40, y = 450)
lblTemp.place(x = 310, y = 450)
lblQotd.place(x = 5, y = 500)
lblCityName.place(x = 90, y =450)
lblCityTemp.place(x = 400, y = 450)
lblQotdDaily.place(x = 5, y = 530)
lblDate.place(x = 380, y = 10)

btnAdd.configure(bg = 'SkyBlue3')
btnView.configure(bg = 'SkyBlue3')
btnUpdate.configure(bg = 'SkyBlue3')
btnDelete.configure(bg = 'SkyBlue3')
btnGraph.configure(bg = 'SkyBlue3')

'''def rnoandmarks(inp):
	if inp.isdigit():       
		return True
		
	elif inp is "":
		return True
	else:
		return False'''

adst = Toplevel(root)
adst.title("Add student ")
adst.geometry("500x500+250+250")
adst.configure(background = 'red2')
lblAddEnterRno = Label(adst, text = "Enter Roll Number", font = ('arial',14,'italic'),width = 20,bg='red2')
entAddRno = Entry(adst, bd = 5, font = ('arial',14,'italic'))
lblAddEnterName = Label(adst, text = "Enter Name", font = ('arial',14,'italic'), width = 15,bg='red2')
entAddName = Entry(adst, bd = 5, font = ('arial',14,'italic')) 
lblAddEnterMarks = Label(adst, text = "Enter marks ", font = ('arial',14,'italic'), width = 15,bg='red2')
entAddMarks = Entry(adst, bd = 5, font = ('arial',14,'italic'))
btnAddBack = Button(adst, text = "Back", font = ('arial',16,'bold'), width = 10, height = 1, command = f2)
btnAddSave = Button(adst, text = "Save", font = ('arial',16,'bold'), width = 10, height = 1, command = f9)
lblAddEnterRno.pack(pady = 10)
entAddRno.pack(pady = 10)
lblAddEnterName.pack(pady = 10)
entAddName.pack(pady = 10)
lblAddEnterMarks.pack(pady = 10)
entAddMarks.pack(pady = 10)
btnAddSave.pack(pady = 10)
btnAddBack.pack(pady = 10)
btnAddSave.configure(bg = 'red3')
btnAddBack.configure(bg = 'red3')
adst.withdraw()

vist = Toplevel(root)
vist.title("View student details")

vist.geometry("500x500+250+250")
vist.configure(background = 'SeaGreen2')
stdata = scrolledtext.ScrolledText(vist, width = 40, height = 20)
btnViewBack = Button(vist, text="Back",font=('arial',16,'bold'), width = 10, command = f4)
stdata.pack(pady = 10)
btnViewBack.pack(pady = 10)
btnViewBack.configure(bg = 'SeaGreen3')
vist.withdraw()


upst = Toplevel(root)
upst.title("Update Student ")

upst.geometry("500x500+250+250")
upst.configure(background = 'gold2')
lblUpdateEnterRno = Label(upst, text = "Enter Roll Number", font = ('arial',14,'italic'),width = 20,bg='gold2')
entUpdateRno = Entry(upst, bd = 5, font = ('arial',14,'italic'))
#lblUpdateEnterName = Label(upst, text = "Enter Name", font = ('arial',14,'italic'), width = 15)
#entUpdateName = Entry(upst, bd = 5, font = ('arial',14,'italic')) 
lblUpdateEnterMarks = Label(upst, text = "Enter marks ", font = ('arial',14,'italic'), width = 15,bg='gold2')
entUpdateMarks = Entry(upst, bd = 5, font = ('arial',14,'italic'))
btnUpdateBack = Button(upst, text = "Back", font = ('arial',16,'bold'), width = 10, height = 1, command = f6)
btnUpdateSave = Button(upst, text = "Save", font = ('arial',16,'bold'), width = 10, height = 1, command = f10)
lblUpdateEnterRno.pack(pady = 10)
entUpdateRno.pack(pady = 10)
#lblUpdateEnterName.pack(pady = 10)
#entUpdateName.pack(pady = 10)
lblUpdateEnterMarks.pack(pady = 10)
entUpdateMarks.pack(pady = 10)
btnUpdateSave.pack(pady = 10)
btnUpdateBack.pack(pady = 10)

btnUpdateBack.configure(bg = 'gold3')
btnUpdateSave.configure(bg = 'gold3')

upst.withdraw()

dlst = Toplevel(root)
dlst.title("Delete Student Record ")

dlst.geometry("500x300+250+250")
dlst.configure(background = 'purple1')

lblDeleteEnterRno = Label(dlst, text = "Enter Roll Number", font = ('arial',14,'italic'),width = 20,bg='purple1')
entDeleteRno = Entry(dlst, bd = 5, font = ('arial',14,'italic'))
btnDeleteBack = Button(dlst, text = "Back", font = ('arial',16,'bold'), width = 10, height = 1, command = f8)
btnDeleteSave = Button(dlst, text = "Delete", font = ('arial',16,'bold'), width = 10, height = 1, command = f11)
lblDeleteEnterRno.pack(pady = 10)
entDeleteRno.pack(pady = 10)
btnDeleteSave.pack(pady = 10)
btnDeleteBack.pack(pady = 10)
btnDeleteBack.configure(bg = 'purple2')
btnDeleteSave.configure(bg = 'purple2')
dlst.withdraw()



def create1():
	con = None
	try:
		con = connect ("test.db")
		
		cursor=con.cursor()
		sql="create table student1(rno int primary key, name text, marks int )"
		cursor.execute(sql)
		
	except Exception as e:
		pass
	finally:
		if con is not None:
			con.close()
			
#create1()
root.mainloop()
