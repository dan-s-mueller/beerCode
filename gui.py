from Tkinter import *
import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import plot_beer_data

def save_inputs():
	# Run parameters
	file_name=entry_file_name.get()
	time_inc=float(entry_time_inc.get())
	brew_id=int(float(entry_brew_id.get()))
	database_flag=database_state.get()
	print str(file_name)+"\n"+str(time_inc)+"\n"+str(brew_id)+"\n"+str(database_flag)
	return file_name, time_inc, brew_id, database_flag
def run_main():
	save_inputs()
	lbl_status_r.config(fg="green",text="Running")
	
	# Disable the inputs while running.
	entry_file_name.config(state="disabled")
	entry_time_inc.config(state="disabled")
	entry_brew_id.config(state="disabled")
	chk_database.config(state="disabled")
	
	# Temperature settings
	float(entry_temp_min.get())
	float(entry_temp_min_tol.get())
	float(entry_temp_max.get())
	float(entry_temp_max_tol.get())
	
	print "doing some stuff..."
def update_plot():
	fig=plot_beer_data.csv_plot(entry_file_name.get())
	plot_canvas=FigureCanvasTkAgg(fig, window)
	plot_canvas.draw()
	plot_canvas.get_tk_widget().grid(row=520,column=0,columnspan=2)
	print("plot refreshed")
	
def stop_main():
	lbl_status_r.config(fg="blue",text="Paused")
	
	# Enable the inputs after stoppings.
	entry_file_name.config(state="normal")
	entry_time_inc.config(state="normal")
	entry_brew_id.config(state="normal")
	chk_database.config(state="normal")
	print "Stopping the program."

# Create root object
window=Tk()
window.title("beerCode")
Grid.rowconfigure(window, 0, weight=0)
Grid.columnconfigure(window, 0, weight=1)

# Header stuff and run info
lbl_header=Label(window, text="Beer Code Inputs",font=("Arial Bold", 20))
lbl_header.grid(column=0, row=0,columnspan=2)
sep_run=ttk.Separator(window, orient="horizontal")
sep_run.grid(column=0,row=1,columnspan=2,sticky="ew")
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
entry_time_inc.insert(END,0)
entry_time_inc.grid(row=3,column=1)

# Brew id
lbl_brew_id=Label(window,text="Brew ID: ")
lbl_brew_id.grid(row=4,column=0)
entry_brew_id=Entry(window,width=30)
entry_brew_id.insert(END,0)
entry_brew_id.grid(row=4,column=1)

# Write to database
database_state = BooleanVar()
database_state.set(True) #set check state
chk_database=Checkbutton(window,text='Write to database?', var=database_state)
chk_database.grid(row=5,column=0,columnspan=2)

# Temperature bounds
sep_temp=ttk.Separator(window, orient="horizontal")
sep_temp.grid(row=50,column=0,columnspan=2,sticky="ew")

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
sep_buttons.grid(row=100,column=0,columnspan=2,sticky="ew")

btn_get_inputs=Button(window,text="Run",command=run_main)
btn_get_inputs.grid(row=110,column=0,columnspan=2)
btn_quit=Button(window,text="Stop",fg="red",command=stop_main)
btn_quit.grid(row=120,column=0,columnspan=2)

# Status of program
lbl_status_r=Label(window,text="Initialized",fg="grey",font=("Arial Bold Italic", 10))
lbl_status_r.grid(row=190,column=0,columnspan=2)

# Plotting action
sep_status=ttk.Separator(window, orient="horizontal")
sep_status.grid(row=500,column=0,columnspan=2,sticky="ew")
f=Figure(figsize=(1,1), dpi=100)
plot_canvas=FigureCanvasTkAgg(f, window)
plot_canvas.draw()
plot_canvas.get_tk_widget().grid(row=520,column=0,columnspan=2)
Grid.rowconfigure(window, 520, weight=1)

btn_plot_beer_data=Button(window,text="Plot Beer Data",command=update_plot)
btn_plot_beer_data.grid(row=530,column=0,columnspan=2)

# Make the window
window.mainloop()
