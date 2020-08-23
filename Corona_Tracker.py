from tkinter import *
from covid import Covid
import matplotlib.pyplot as plt
import sqlite3
from PIL import ImageTk,Image
from tkinter.messagebox import showinfo


root = Tk()
root.title("Covid19   Tracker")
root.iconbitmap('C:/Users/User/AppData/Roaming/JetBrains/PyCharm2020.1/scratches/corona.png')
root.geometry('340x350')

frames = LabelFrame(root, text="Search Results", padx=90, pady=45)
frames.grid(row=1, column=0, columnspan=2)

#create a database to store everyday data 
conn = sqlite3.connect('corona_database.db')

#create a cursor
c = conn.cursor()

#create tables in database
#c.execute("CREATE TABLE data (everyday INTEGER)")
#c.execute("CREATE TABLE deaths (Death_count INTEGER)")
#c.execute("CREATE TABLE active_cases (Active_Cases INTEGER)")

#create list to store data
total_cases_list = []
total_deaths_list = []
active_cases_list = []

#getting the data from the covid library
try:
    covid = Covid()
    total_cases = covid.get_total_confirmed_cases()
    total_deaths = covid.get_total_deaths()
    active_cases = covid.get_total_active_cases()
except Exception:
    showinfo("ERROR", "No Internet Connection") 


#Add data to the database
def insert():
    conn = sqlite3.connect('corona_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO data VALUES (:everyday)",{'everyday':total_cases})
    conn.commit()
    c.execute("INSERT INTO deaths VALUES (:Death_count)",{'Death_count':total_deaths})
    conn.commit()
    c.execute("INSERT INTO active_cases VALUES (:Active_Cases)",{'Active_Cases':active_cases})
    conn.commit()
    conn.close()

#Get data from the database
c.execute("SELECT * FROM data")
data1 = c.fetchall()
c.execute("SELECT * FROM deaths")
data2 = c.fetchall()
c.execute("SELECT * FROM active_cases")
data3 = c.fetchall()
          
#Append the data to lists
total_cases_list.append(data1)
total_deaths_list.append(data2)
active_cases_list.append(data3)


#create a function  to delete data
def delete1():
    conn = sqlite3.connect('corona_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM data")
    conn.commit()
    conn.close()

def delete2():
    conn = sqlite3.connect('corona_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM deaths")
    conn.commit()
    conn.close()

def delete3():
    conn = sqlite3.connect('corona_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM active_cases")
    conn.commit()
    conn.close()
    
#create a list by removing the tuples from the data from the database
y1 = []
y2 = []
y3 = []

for i in range(len(data1)):
    y1.append(data1[i][0])

for i in range(len(data2)):
    y2.append(data2[i][0])

for i in range(len(data3)):
    y3.append(data3[i][0])

#list of values in X-axis
x1 = [h for h in range(len(y1)+1)]
x2 = [h for h in range(len(y2)+1)]
x3 = [h for h in range(len(y3)+1)]
x1 = x1[1:]
x2 = x2[1:]
x3 = x3[1:]

#print(x1)
#print(x2)

#creating a function for plotting graph of total_cases
def graph1():
    plt.plot(x1, y1, marker='o', markerfacecolor="#f48371", markersize=12)
    plt.title("Total Covid Cases", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("No of Cases (crore)", fontsize=14)
    plt.grid()
    plt.show()

#creating a function for plotting graph of total_deaths
def graph2():
    plt.plot(x2, y2, marker='o', markerfacecolor="#9d3ca1", markersize=12)
    plt.title("Death Counts", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("No of Deaths", fontsize=14)
    plt.grid()
    plt.show() 

#creating a function for plotting graph of active_cases
def graph3():
    plt.plot(x3, y3, marker='o', markerfacecolor="#f48371", markersize=12)
    plt.title("Active Cases", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("No of Cases (million)", fontsize=14)
    plt.grid()
    plt.show()

#create a function for getting data of searched country
def search():
    try:
        country = str(search_country.get())
        status = covid.get_status_by_country_name(country)
        country_label = Label(frames, text=f"Country: {status['country']}")
        country_label.grid(row=0,column=0)
        confirmed_label = Label(frames, text=f"Confimed Cases: {status['confirmed']}")
        confirmed_label.grid(row=1, column=0)
        death_label = Label(frames, text=f"Deaths: {status['deaths']}")
        death_label.grid(row=2, column=0)
        active_label = Label(frames, text=f"Active Cases: {status['active']}")
        active_label.grid(row=3, column=0)
    except Exception:
        error_label = Label(frames, text="Country name not found")
        error_label.pack()
   
#Create labels
label1 = Label(root,borderwidth=5, text="Total Cases:  " + str(total_cases) + "    ")
label1.grid(row=2, column=0)
label2 = Label(root,borderwidth=5, text="Death Count:  " + str(total_deaths) + "    ")
label2.grid(row=3,column=0)
label3 = Label(root,borderwidth=5, text="Active Cases:  " + str(active_cases) + "    ")
label3.grid(row=4, column=0)

#create a button to show the graph of total cases
button1 = Button(root, text="Show Graph", command=graph1)
button1.grid(row=2, column=1)
button2 = Button(root, text="Show Graph", command=graph2)
button2.grid(row=3, column=1)
button3 = Button(root, text="Show Graph", command=graph3)
button3.grid(row=4, column=1)

#entry box
search_country = Entry(root, borderwidth=30)
search_country.grid(row=0,column=0, columnspan=2)
search_country.insert(0, "enter a country name")

#search button for countries
search_button = Button(root, text="Search", command=search)
search_button.grid(row=0, column=1)

 #create a button to add the data to the database
add_button = Button(root, text="Add To Database", command=insert)
add_button.grid(row=3, column=2)


#create a button to delete data
button11 = Button(root, text="Delete Data1", command=delete1)
#button11.grid(row=5, column=0)
button21 = Button(root, text="Delete Data2", command=delete2)
#button21.grid(row=5, column=1)
button31 = Button(root, text="Delete Data3", command=delete3)
#button31.grid(row=5, column=2)

conn.commit()

conn.close() 

root.mainloop()
