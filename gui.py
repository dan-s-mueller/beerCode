from Tkinter import *
import RPi.GPIO as GPIO
import mysql.connector
import ttk
import time
import datetime
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import plot_beer_data
import main

# Global variables
mydb_global=None
mycursor_global=None
logger_global=None
fout_global=None
relay_cool_global=None
relay_hot_global=None
delay_global=50
is_initializing_global=True
running=False

def scanning():
	global running, delay_global, is_initializing_global
	global fout_global, logger_global, relay_cool_global, relay_hot_global, mydb_global, mycursor_global
	
	if (not running) and (not is_initializing_global):
		# do something after request to stop has been received
		lbl_status_r.config(fg="blue",text="Paused, Last Updated: "+ \
			'{date:%Y-%m-%d, %H:%M:%S}'.format(date=datetime.datetime.now()))
		
		# Enable the inputs after stoppings.
		entry_file_name.config(state="normal")
		entry_time_inc.config(state="normal")
		entry_brew_id.config(state="normal")
		chk_database.config(state="normal")
		

		lbl_temp_air.config(text="Air temp: "+"Paused",fg="grey")
		lbl_temp_liquid.config(text="Air temp: "+"Paused",fg="grey")
		lbl_heat.config(text="Heater status: "+"Off",fg="grey")
		lbl_cool.config(text="Cooler status: "+"Off",fg="grey")
		
		is_initializing_global=True
		delay_global=50

		try:
			fout_global.close()
			if database_state.get():
				database_state.set(False) #set check state
				mydb_global.close()
			GPIO.cleanup()
			print("Cleanup complete and program stopped.")
		except Exception as e: 
			print e
			print("Cleanup had errors but program stopped.")
	elif running:
		file_name=entry_file_name.get()
		time_inc=float(entry_time_inc.get())
		brew_id=int(float(entry_brew_id.get()))
		database_flag=database_state.get()
		sql_user=entry_sql_user.get()
		sql_password=entry_sql_password.get()
		
		lbl_status_r.config(fg="green",text="Running, Last Updated: "+ \
			'{date:%Y-%m-%d, %H:%M:%S}'.format(date=datetime.datetime.now()))
		
		# Disable the inputs while running.
		entry_file_name.config(state="disabled")
		entry_time_inc.config(state="disabled")
		entry_brew_id.config(state="disabled")
		chk_database.config(state="disabled")
		entry_sql_user.config(state="disabled")
		entry_sql_password.config(state="disabled")
		
		# Temperature settings
		temp_min=float(entry_temp_min.get())
		temp_min_tol=float(entry_temp_min_tol.get())
		temp_max=float(entry_temp_max.get())
		temp_max_tol=float(entry_temp_max_tol.get())
		
		# Initialize the inputs and run the main program
		if database_state.get():
			# Initialize and run the system. Will run in infinite loop until interrupted
			if is_initializing_global:
				fout_global,logger_global,relay_cool_global,relay_hot_global,mydb_global,mycursor_global= \
					main.initialize(file_name,time_inc,brew_id,database_flag,sql_user,sql_password)
				is_initializing_global=False
				print "Main program initialized."
			fout_global,temperature_air,temperature_liquid,stat_heat,stat_cool= \
				main.run_system(fout_global,logger_global,relay_cool_global,relay_hot_global,file_name,temp_min,temp_min_tol,temp_max,temp_max_tol,brew_id,database_state.get(),mydb_global,mycursor_global)
		else:
			# Initialize and run the system. Will run in infinite loop until interrupted
			if is_initializing_global:
				fout_global,logger_global,relay_cool_global,relay_hot_global= \
						main.initialize(file_name,time_inc,brew_id,database_flag,sql_user,sql_password)
				is_initializing_global=False
				print "Main program initialized."
			fout_global,temperature_air,temperature_liquid,stat_heat,stat_cool= \
					main.run_system(fout_global,logger_global,relay_cool_global,relay_hot_global,file_name,temp_min,temp_min_tol,temp_max,temp_max_tol,brew_id,0,0,0)
		# Show temperatures and status
		lbl_temp_air.config(text="Air temp: "+format(temperature_air,".2f"),fg="black")
		lbl_temp_liquid.config(text="Liquid temp: "+format(temperature_liquid,".2f"),fg="black")	
		if stat_heat:
			lbl_heat.config(text="Heater status: "+"On",fg="red")
		else:
			lbl_heat.config(text="Heater status: "+"Off",fg="gray")
		if stat_cool:
			lbl_cool.config(text="Cooler status: "+"On",fg="blue")
		else:
			lbl_cool.config(text="Cooler status: "+"Off",fg="gray")
		delay_global=int(float(entry_time_inc.get())*1000)
	window.after(delay_global, scanning)
    
def update_sql_fields():
	if database_state.get() == 1:          #whenever checked
		entry_sql_user.config(state=NORMAL)
		entry_sql_password.config(state=NORMAL)
	elif database_state.get() == 0:        #whenever unchecked
		entry_sql_user.config(state=DISABLED)
		entry_sql_password.config(state=DISABLED)
	
def start_main():
    # Sets run to true so that scan can execute.
	global running
	running=True
	
def update_plot():    
	fig=plot_beer_data.csv_plot(entry_file_name.get())
	plot_canvas=FigureCanvasTkAgg(fig, window)
	plot_canvas.draw()
	plot_canvas.get_tk_widget().grid(row=520,column=0,columnspan=100)
	print("Plot refreshed")
	
def stop_main():
	# Pauses the program but does not close the window
	global running
	
	running=False

	lbl_status_r.config(fg="red",text="Request to stop received: "+ \
			'{date:%Y-%m-%d, %H:%M:%S}'.format(date=datetime.datetime.now()))

def kill_main():
	# Cleans up ports but kills window.
	global running
	
	running=False
	delay_global=50

	try:
		fout_global.close()
		if database_state.get():
			database_state.set(False) #set check state
			mydb_global.close()
		GPIO.cleanup()
		print("Cleanup complete and program stopped.")
	except Exception as e: 
		print e
		print("Cleanup had errors but program stopped.")
	window.destroy()

# Create root object
window=Tk()
window.title("beerCode")
Grid.rowconfigure(window, 0, weight=0)
Grid.columnconfigure(window, 0, weight=1)

# Header stuff and run info
lbl_header=Label(window, text="Beer Code Inputs",font=("Arial Bold", 20))
lbl_header.grid(column=0, row=0,columnspan=100)
sep_run=ttk.Separator(window, orient="horizontal")
sep_run.grid(column=0,row=1,columnspan=100,sticky="ew")
#Grid.rowconfigure(window,0,weight=0)
#Grid.rowconfigure(window,1,weight=0)

# File name entry.
lbl_file_name=Label(window,text="File name: ")
lbl_file_name.grid(row=2,column=0)
entry_file_name=Entry(window,width=30)
entry_file_name.insert(END,"my_file_name")
entry_file_name.grid(row=2,column=1)
        
# Time increment
lbl_time_inc=Label(window,text="Time increment (s): ")
lbl_time_inc.grid(row=3,column=0)
entry_time_inc=Entry(window,width=30)
entry_time_inc.insert(END,60)
entry_time_inc.grid(row=3,column=1)

# Brew id
lbl_brew_id=Label(window,text="Brew ID: ")
lbl_brew_id.grid(row=4,column=0)
entry_brew_id=Entry(window,width=30)
entry_brew_id.insert(END,0)
entry_brew_id.grid(row=4,column=1)

# Database parameters
database_state = BooleanVar()
database_state.set(False) #set check state
chk_database=Checkbutton(window,text='Write to database?', var=database_state,command=update_sql_fields)
chk_database.grid(row=2,column=2)

lbl_sql_user=Label(window,text="Sql user: ")
lbl_sql_user.grid(row=3,column=2)
entry_sql_user=Entry(window,width=30)
entry_sql_user.insert(END,"dmueller")
entry_sql_user.config(state="disabled")
entry_sql_user.grid(row=3,column=3)
lbl_sql_password=Label(window,text="Sql password: ")
lbl_sql_password.grid(row=4,column=2)
entry_sql_password=Entry(window,width=30,show="*",state="disabled")
entry_sql_password.grid(row=4,column=3)

# Temperature bounds
sep_temp=ttk.Separator(window, orient="horizontal")
sep_temp.grid(row=50,column=0,columnspan=100,sticky="ew")

lbl_temp_min=Label(window,text="Min Temperature (F): ")
lbl_temp_min.grid(row=60,column=0)
entry_temp_min=Entry(window,width=15)
entry_temp_min.insert(END,-100)
entry_temp_min.grid(row=60,column=1)
lbl_temp_min_tol=Label(window,text="Min Temperature Offset (F): ")
lbl_temp_min_tol.grid(row=70,column=0)
entry_temp_min_tol=Entry(window,width=15)
entry_temp_min_tol.insert(END,1)
entry_temp_min_tol.grid(row=70,column=1)
lbl_temp_max=Label(window,text="Max Temperature (F): ")
lbl_temp_max.grid(row=80,column=0)
entry_temp_max=Entry(window,width=15)
entry_temp_max.insert(END,100)
entry_temp_max.grid(row=80,column=1)
lbl_temp_max_tol=Label(window,text="Max Temperature Offset (F): ")
lbl_temp_max_tol.grid(row=90,column=0)
entry_temp_max_tol=Entry(window,width=15)
entry_temp_max_tol.insert(END,-1)
entry_temp_max_tol.grid(row=90,column=1)



# Action buttons
sep_buttons=ttk.Separator(window, orient="horizontal")
sep_buttons.grid(row=100,column=0,columnspan=100,sticky="ew")

btn_get_inputs=Button(window,text="Run",command=start_main)
btn_get_inputs.grid(row=110,column=0)
btn_quit=Button(window,text="Stop",fg="red",command=stop_main)
btn_quit.grid(row=120,column=0)

# Show the temps
lbl_temp_air=Label(window,text="Air temp: "+"Not running",fg="grey")
lbl_temp_air.grid(row=110,column=1)
lbl_temp_liquid=Label(window,text="Liquid temp: "+"Not running",fg="grey")
lbl_temp_liquid.grid(row=120,column=1)
lbl_heat=Label(window,text="Heater status: "+"Off",fg="grey")
lbl_heat.grid(row=110,column=2)
lbl_cool=Label(window,text="Cooler status: "+"Off",fg="grey")
lbl_cool.grid(row=120,column=2)

# Status of program
lbl_status_r=Label(window,text="Initialized",fg="grey",font=("Arial Bold Italic", 10))
lbl_status_r.grid(row=190,column=0,columnspan=100)

# Plotting action
sep_status=ttk.Separator(window, orient="horizontal")
sep_status.grid(row=500,column=0,columnspan=100,sticky="ew")
f=Figure(figsize=(1,0.75), dpi=100)
plot_canvas=FigureCanvasTkAgg(f, window)
plot_canvas.draw()
plot_canvas.get_tk_widget().grid(row=520,column=0,columnspan=100)
Grid.rowconfigure(window, 520, weight=1)

btn_plot_beer_data=Button(window,text="Plot Beer Data",command=update_plot)
btn_plot_beer_data.grid(row=530,column=0,columnspan=100)

# Make the window and set close behavior
window.after(delay_global, scanning)
window.protocol("WM_DELETE_WINDOW", kill_main)
window.mainloop()
