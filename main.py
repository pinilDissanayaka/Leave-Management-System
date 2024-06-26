from utils.model import Database
from utils.app import EmployeeApp
import tkinter as tk

db=Database(user='root')

root = tk.Tk()
employeeApp = EmployeeApp(root)
root.mainloop()

