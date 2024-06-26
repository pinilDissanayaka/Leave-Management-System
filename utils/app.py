import tkinter as tk
from tkinter import messagebox, ttk
from mysql import connector
from datetime import datetime

class EmployeeApp(object):
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Leave Management System")

        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Employee Number").grid(row=0, column=0)
        self.employee_number = tk.Entry(self.root)
        self.employee_number.grid(row=0, column=1)

        tk.Label(self.root, text="Password").grid(row=1, column=0)
        self.password = tk.Entry(self.root, show="*")
        self.password.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=1)

    def login(self):
        emp_num = self.employee_number.get()
        pwd = self.password.get()

        conn = connector.connect('leave_management.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM employees WHERE employee_number = ? AND password = ?", (emp_num, pwd))
        result = cursor.fetchone()
        
        conn.close()

        if result:
            self.employee_id = result[0]
            self.employee_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid employee number or password.")

    def employee_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Employee Dashboard").grid(row=0, column=0, columnspan=2)

        tk.Button(self.root, text="Apply for Leave", command=self.apply_leave_screen).grid(row=1, column=0)
        tk.Button(self.root, text="View Leave Status", command=self.view_leave_status).grid(row=1, column=1)
        tk.Button(self.root, text="Delete Applied Leaves", command=self.delete_leave_screen).grid(row=2, column=0)
        tk.Button(self.root, text="View Remaining Leaves", command=self.view_remaining_leaves).grid(row=2, column=1)
        tk.Button(self.root, text="View Leave History", command=self.view_leave_history).grid(row=3, column=0, columnspan=2)

    def apply_leave_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Apply for Leave").grid(row=0, column=0, columnspan=2)

        tk.Label(self.root, text="Leave Type").grid(row=1, column=0)
        self.leave_type = ttk.Combobox(self.root, values=["Annual Leave", "Casual Leave", "Short Leave"])
        self.leave_type.grid(row=1, column=1)

        tk.Label(self.root, text="Start Date (YYYY-MM-DD)").grid(row=2, column=0)
        self.start_date = tk.Entry(self.root)
        self.start_date.grid(row=2, column=1)

        tk.Label(self.root, text="End Date (YYYY-MM-DD)").grid(row=3, column=0)
        self.end_date = tk.Entry(self.root)
        self.end_date.grid(row=3, column=1)

        tk.Button(self.root, text="Apply", command=self.apply_leave).grid(row=4, column=1)

    def apply_leave(self):
        leave_type = self.leave_type.get()
        start_date = self.start_date.get()
        end_date = self.end_date.get()

        conn = connector.connect('leave_management.db')
        cursor = conn.cursor()

        # Validate and apply leave
        if leave_type == "Annual Leave":
            cursor.execute("SELECT COUNT(*) FROM leaves WHERE employee_id = ? AND leave_type = 'Annual Leave' AND status = 'Approved' AND start_date >= date('now','start of year') AND end_date <= date('now','start of year','+1 year')", (self.employee_id,))
            annual_leaves_taken = cursor.fetchone()[0]
            if annual_leaves_taken >= 14:
                messagebox.showerror("Leave Error", "You have exceeded your annual leave quota.")
                conn.close()
                return

        elif leave_type == "Casual Leave":
            cursor.execute("SELECT COUNT(*) FROM leaves WHERE employee_id = ? AND leave_type = 'Casual Leave' AND status = 'Approved' AND start_date >= date('now','start of year') AND end_date <= date('now','start of year','+1 year')", (self.employee_id,))
            casual_leaves_taken = cursor.fetchone()[0]
            if casual_leaves_taken >= 7:
                messagebox.showerror("Leave Error", "You have exceeded your casual leave quota.")
                conn.close()
                return

        elif leave_type == "Short Leave":
            cursor.execute("SELECT COUNT(*) FROM leaves WHERE employee_id = ? AND leave_type = 'Short Leave' AND status = 'Approved' AND start_date >= date('now','start of month') AND end_date <= date('now','start of month','+1 month')", (self.employee_id,))
            short_leaves_taken = cursor.fetchone()[0]
            if short_leaves_taken >= 2:
                messagebox.showerror("Leave Error", "You have exceeded your short leave quota.")
                conn.close()
                return

        cursor.execute("INSERT INTO leaves (employee_id, leave_type, start_date, end_date, status) VALUES (?, ?, ?, ?, 'Pending')", (self.employee_id, leave_type, start_date, end_date))
        conn.commit()
        conn.close()
        messagebox.showinfo("Leave Applied", "Your leave has been applied successfully.")
        self.employee_dashboard()

    def view_leave_status(self):
        self.clear_screen()
        tk.Label(self.root, text="Leave Status").grid(row=0, column=0, columnspan=2)

        conn = connector.connect('leave_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT leave_type, start_date, end_date, status FROM leaves WHERE employee_id = ?", (self.employee_id,))
        leaves = cursor.fetchall()

        conn.close()

        for idx, leave in enumerate(leaves):
            tk.Label(self.root, text=leave[0]).grid(row=idx+1, column=0)
            tk.Label(self.root, text=f"{leave[1]} to {leave[2]}").grid(row=idx+1, column=1)
            tk.Label(self.root, text=leave[3]).grid(row=idx+1, column=2)

        tk.Button(self.root, text="Back", command=self.employee_dashboard).grid(row=len(leaves)+1, column=1)

    def delete_leave_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Delete Leave").grid(row=0, column=0, columnspan=2)

        tk.Label(self.root, text="Leave ID").grid(row=1, column=0)
        self.leave_id = tk.Entry(self.root)
        self.leave_id.grid(row=1, column=1)

        tk.Button(self.root, text="Delete", command=self.delete_leave).grid(row=2, column=1)

    def delete_leave(self):
        leave_id = self.leave_id.get()

        conn = connector.connect('leave_management.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM leaves WHERE id = ? AND employee_id = ? AND status = 'Pending'", (leave_id, self.employee_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Leave Deleted", "The leave has been deleted successfully.")
        self.employee_dashboard()

    def view_remaining_leaves(self):
        self.clear_screen()
        tk.Label(self.root, text="Remaining Leaves").grid(row=0, column=0, columnspan=2)

        conn = connector.connect('leave_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT annual_leaves, casual_leaves, short_leaves FROM employees WHERE id = ?", (self.employee_id,))
        remaining_leaves = cursor.fetchone()

        conn.close()

        tk.Label(self.root, text=f"Annual Leaves: {remaining_leaves[0]}").grid(row=1, column=0)
        tk.Label(self.root, text=f"Casual Leaves: {remaining_leaves[1]}").grid(row=2, column=0)
        tk.Label(self.root, text=f"Short Leaves: {remaining_leaves[2]}").grid(row=3, column=0)

        tk.Button(self.root, text="Back", command=self.employee_dashboard).grid(row=4, column=1)

    def view_leave_history(self):
        self.clear_screen()
        tk.Label(self.root, text="Leave History").grid(row=0, column=0, columnspan=2)

        conn = connector.connect('leave_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT leave_type, start_date, end_date, status FROM leaves WHERE employee_id = ?", (self.employee_id,))
        leaves = cursor.fetchall()

        conn.close()

        for idx, leave in enumerate(leaves):
            tk.Label(self.root, text=leave[0]).grid(row=idx+1, column=0)
            tk.Label(self.root, text=f"{leave[1]} to {leave[2]}").grid(row=idx+1, column=1)
            tk.Label(self.root, text=leave[3]).grid(row=idx+1, column=2)

        tk.Button(self.root, text="Back", command=self.employee_dashboard).grid(row=len(leaves)+1, column=1)

