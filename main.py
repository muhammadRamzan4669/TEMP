import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import pymssql

class ASKAcademyApp:
  def __init__(self, root):
    self.root = root
    self.root.title("ASK Academy School Management System")
    self.root.geometry("800x600")
    self.root.configure(bg="white")
    self.root.grid_rowconfigure(1, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    ctk.set_appearance_mode("light")  # or "dark"
    ctk.set_default_color_theme("blue")  # or "green", "dark-blue"


    # Database connection using pymssql for Azure SQL 
    try:
      self.conn = pymssql.connect(
        server="ask-academy.database.windows.net",
        port=1433,
        database="ASK_Academy",
        user="ask-academy",
        password="UniP@ssw0rd!2025",
        tds_version="7.4"
      )
      self.cursor = self.conn.cursor()
      print("Connected to Azure SQL Database successfully!")
    except pymssql.Error as e:
      messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
      self.root.destroy()
      return

    self.create_main_dashboard()

  def menu_bar(self, active_button=None):

    # Create responsive menu bar frame
    menu_frame = ctk.CTkFrame(self.root, fg_color="#2c3e50", height=40)
    menu_frame.grid(row=0, column=0, sticky="ew")
    
    menu_items = [
      ("Dashboard", self.create_main_dashboard),
      ("Students", self.student_screen),
      ("Teachers", self.teacher_screen),
      ("Batches", self.batch_screen),
      ("Rooms", self.room_screen),
      ("Classes", self.class_screen),
      ("Timetable", self.timetable_screen),
      ("Tests", self.test_screen),
      ("Attendance", self.attendance_screen),
      ("Teacher Attendance", self.teacher_attendance_screen),
      ("Salaries", self.salary_screen),
      ("Classroom Assets", self.asset_screen),
      ("Maintenance", self.maintenance_screen),
      ("Fees", self.fee_screen),
      ("Expenses", self.expense_screen),
    ]

    for idx, (text, command) in enumerate(menu_items):
      btn = ctk.CTkButton(
        menu_frame,
        text=text,
        command=command,
        font=ctk.CTkFont("Arial", 12),
        height=40,
        corner_radius=0,
        fg_color="#2980b9" if text == active_button else "#34495e",
        hover_color="#1abc9c",
        text_color="white"
      )
      btn.grid(row=0, column=idx, sticky="nsew", padx=1)

  def create_main_dashboard(self):
    for widget in self.root.winfo_children():
      widget.destroy()

    self.root.attributes('-zoomed', True)

    self.root.grid_rowconfigure(0, weight=0)  # Menu bar
    self.root.grid_rowconfigure(1, weight=1)  # Content frame
    self.root.grid_columnconfigure(0, weight=1)

    self.menu_bar("Dashboard")

    # Main frame that holds the entire dashboard content
    content_frame = ctk.CTkFrame(self.root, fg_color="white")
    content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    content_frame.grid_rowconfigure(0, weight=0)  # Title
    content_frame.grid_rowconfigure(1, weight=1)  # Buttons
    content_frame.grid_rowconfigure(2, weight=1)  # Extra space below
    content_frame.grid_columnconfigure(0, weight=1)  # Left padding
    content_frame.grid_columnconfigure(1, weight=0)  # Content
    content_frame.grid_columnconfigure(2, weight=1)  # Right padding
    
    # Title label
    title_label = ctk.CTkLabel(content_frame, text="ASK Academy Management System",
                   font=("Arial", 24), text_color="blue")
    title_label.grid(row=0, column=2, pady=20, sticky="ew")

    # Button definitions
    buttons = [
      ("Students \n\n 200", self.student_screen),
      ("Teachers \n\n 20", self.teacher_screen),
      ("Batches \n\n 19", self.batch_screen),
      ("Rooms \n\n 20", self.room_screen),
      ("Classes \n\n 4", self.class_screen),
    ]

    # Grid-based button layout
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.grid(row=1, column=3, columnspan=3, pady=10)

    for row in range((len(buttons) + 2) // 3):
      button_frame.grid_rowconfigure(row, weight=1)
    for col in range(3):
      button_frame.grid_columnconfigure(col, weight=1)
    
    for i, (text, command) in enumerate(buttons):
      row = i // 3
      col = i % 3
      button = ctk.CTkButton(
        button_frame,
        text=text,
        width=200,
        height=100,
        command=command,
        fg_color="#34495e",
        hover_color="#2c3e50",
        text_color="white",
        font=("Arial", 14)
      )
      button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

  
  # Helper methods for dropdown values
  def get_batch_ids(self):
    self.cursor.execute("SELECT BatchID FROM dbo.Batch")
    return [str(row[0]) for row in self.cursor.fetchall()]

  def get_room_ids(self):
    self.cursor.execute("SELECT RoomID FROM dbo.Room")
    return [str(row[0]) for row in self.cursor.fetchall()]

  def get_class_ids(self):
    self.cursor.execute("SELECT ClassID FROM dbo.Class")
    return [str(row[0]) for row in self.cursor.fetchall()]

  def get_student_ids(self):
    self.cursor.execute("SELECT StudentID FROM dbo.Student")
    return [row[0] for row in self.cursor.fetchall()]

  def get_teacher_ids(self):
    self.cursor.execute("SELECT TeacherID FROM dbo.Teacher")
    return [str(row[0]) for row in self.cursor.fetchall()]

  def get_asset_ids(self):
    self.cursor.execute("SELECT AssetID FROM dbo.ClassroomAsset")
    return [str(row[0]) for row in self.cursor.fetchall()]

  # Generic screen creation function
  def create_manage_screen(self, title, table_name, columns, fields_info, queries):

    for widget in self.root.winfo_children():
      widget.destroy()

    self.menu_bar(title)

    self.root.grid_rowconfigure(0, weight=0)  # Menu bar
    self.root.grid_rowconfigure(1, weight=0)  # Title
    self.root.grid_rowconfigure(2, weight=0)  # Form
    self.root.grid_rowconfigure(3, weight=0)  # Buttons
    
    
    ctk.CTkLabel(self.root, text=title, font=("Arial", 16), fg_color="white", text_color="blue").grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Form
    form_frame = ctk.CTkFrame(self.root, fg_color="white")
    form_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    self.fields = {}
    for i, (label, field_type, options) in enumerate(fields_info):
      ctk.CTkLabel(form_frame, text=label + ":", fg_color="white").grid(row=i, column=0, padx=5, pady=5, sticky="w")
      if field_type == "entry":
        self.fields[label] = ctk.CTkEntry(form_frame)
      elif field_type == "combobox":
        self.fields[label] = ttk.Combobox(form_frame, values=options() if callable(options) else options)
      self.fields[label].grid(row=i, column=1, padx=5, pady=5, sticky="ew")

    # Mark primary key fields as read-only in edit mode
    pk_fields = [col for col in columns[:len([f for f in fields_info if f[1] == "entry" and "ID" in f[0]])]]

    # Buttons
    button_frame = ctk.CTkFrame(self.root, fg_color="white")
    button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    self.mode = 'add'
    self.selected_pk = None

    def new_record():
      for field in self.fields.values():
        if isinstance(field, ctk.CTkEntry):
          field.delete(0, ctk.END)
          field.config(state='normal')
        elif isinstance(field, ttk.Combobox):
          field.set('')
      self.mode = 'add'
      self.selected_pk = None
      save_button.config(text=f"Add {table_name[:-1]}")

    def save_record():
      values = [field.get() for field in self.fields.values()]

      if self.mode == 'add':
        try:
          # Exclude auto-increment IDs from insert
          # insert_values = [v for i, v in enumerate(values) 
          #          if not fields_info[i][0].endswith("ID")]
          #modified by lynx
    
          insert_values = values
              
          self.cursor.execute(queries["insert"], insert_values)
          self.conn.commit()
          messagebox.showinfo("Success", f"{table_name[:-1]} added")
          refresh_table()
          new_record()
        except Exception as e:
          messagebox.showerror("Error", str(e))

      elif self.mode == 'edit':
        try:
          # Get values in SET ... WHERE ... order
          update_values = values[len(pk_fields):] + values[:len(pk_fields)]
          self.cursor.execute(queries["update"], update_values)
          self.conn.commit()
          messagebox.showinfo("Success", f"{table_name[:-1]} updated")
          refresh_table()
          new_record()
        except Exception as e:
          messagebox.showerror("Error", str(e))
    # def save_record():
      # print('save_record called')
      # values = [field.get() for field in self.fields.values()]
      # print("Inserting values:", values)
      # if self.mode == 'add':
      #     try:
      #         self.cursor.execute(queries["insert"], values)
      #         self.conn.commit()
      #         messagebox.showinfo("Success", f"{table_name[:-1]} added successfully")
      #         refresh_table()
      #         new_record()
      #     except pymssql.Error as e:
      #         messagebox.showerror("Error", str(e))
      # elif self.mode == 'edit':
      #     update_values = values[len(pk_fields):] + [values[i] for i in range(len(pk_fields))]
      #     try:
      #         self.cursor.execute(queries["update"], update_values)
      #         self.conn.commit()
      #         messagebox.showinfo("Success", f"{table_name[:-1]} updated successfully")
      #         refresh_table()
      #         new_record()
      #     except pymssql.Error as e:
      #         messagebox.showerror("Error", str(e))

      # for debugging only

    def delete_record():
      if self.selected_pk:
        try:
          self.cursor.execute(queries["delete"], self.selected_pk if len(pk_fields) == 1 else self.selected_pk)
          self.conn.commit()
          messagebox.showinfo("Success", f"{table_name[:-1]} deleted successfully")
          refresh_table()
          new_record()
        except pymssql.Error as e:
          messagebox.showerror("Error", str(e))
      else:
        messagebox.showwarning("Warning", "No record selected")

    new_button = ctk.CTkButton(button_frame, text="New", fg_color="blue", text_color="white", command=new_record)
    new_button.grid(row=0, column=0, padx=5, pady=5)

    save_button = ctk.CTkButton(button_frame, text=f"Add {table_name}", fg_color="blue", text_color="white", command=save_record)
    save_button.grid(row=0, column=1, padx=5, pady=5)

    delete_button = ctk.CTkButton(button_frame, text="Delete", fg_color="blue", text_color="white", command=delete_record)
    delete_button.grid(row=0, column=2, padx=5, pady=5)

    back_button = ctk.CTkButton(button_frame, text="Back to Menu", fg_color="blue", text_color="white", command=self.create_main_dashboard)
    back_button.grid(row=0, column=3, padx=5, pady=5)

    # Table
    tree_frame = ctk.CTkFrame(self.root, fg_color="white")
    tree_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
    #tree_frame.pack_propagate(False)
    tree_frame.columnconfigure(0, weight=1)
    tree_frame.rowconfigure(0, weight=1)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
      tree.heading(col, text=col)
    tree.grid(row=0, column=0, sticky="nsew")

    def refresh_table():
      for item in tree.get_children():
        tree.delete(item)
      self.cursor.execute(queries["select"])
      rows = self.cursor.fetchall()
      for row in rows:
        tree.insert("", "end", values=row)

    def on_select(event):
      selected_item = tree.selection()
      if selected_item:
          values = tree.item(selected_item[0])['values']
          for i, (label, _, _) in enumerate(fields_info):
              if isinstance(self.fields[label], ctk.CTkEntry):
                  self.fields[label].delete(0, ctk.END)
                  self.fields[label].insert(0, values[i])
                  if label in pk_fields:
                      self.fields[label].config(state='disabled')
              elif isinstance(self.fields[label], ttk.Combobox):
                  self.fields[label].set(values[i])
          self.mode = 'edit'
          self.selected_pk = values[:len(pk_fields)] if len(pk_fields) > 1 else values[0]
          save_button.config(text=f"Update {table_name[:-1]}")
      else:
          new_record()

    tree.bind('<<TreeviewSelect>>', on_select)
    refresh_table()
  

  # Screen definitions
  def batch_screen(self):

    self.create_manage_screen(
      "Batches", "Batch",
      ("BatchID", "Year", "Program"),
      [("BatchID", "entry", None), ("Year", "entry", None), ("Program", "combobox", ["Matric", "Intermediate"])],
      {
        "select": "SELECT BatchID, Year, Program FROM dbo.Batch",
        "insert": "INSERT INTO dbo.Batch (BatchID, Year, Program) VALUES (%s, %s, %s)",
        "update": "UPDATE dbo.Batch SET Year = %s, Program = %s WHERE BatchID = %s",
        "delete": "DELETE FROM dbo.Batch WHERE BatchID = %s"
      }
    )

  def room_screen(self):

    self.create_manage_screen(
      "Rooms", "Room",
      ("RoomID", "Capacity", "AC_Count", "Chair_Count"),
      [("RoomID", "entry", None), ("Capacity", "combobox", [40, 60, 80]), ("AC_Count", "entry", None), ("Chair_Count", "entry", None)],
      {
        "select": "SELECT RoomID, Capacity, AC_Count, Chair_Count FROM dbo.Room",
        "insert": "INSERT INTO dbo.Room (RoomID, Capacity, AC_Count, Chair_Count) VALUES (%s, %s, %s, %s)",
        "update": "UPDATE dbo.Room SET Capacity = %s, AC_Count = %s, Chair_Count = %s WHERE RoomID = %s",
        "delete": "DELETE FROM dbo.Room WHERE RoomID = %s"
      }
    )

  def class_screen(self):

    self.create_manage_screen(
      "Classes", "Class",
      ("ClassID", "BatchID", "Section", "RoomID"),
      [("ClassID", "entry", None), ("BatchID", "combobox", self.get_batch_ids), ("Section", "entry", None), ("RoomID", "combobox", self.get_room_ids)],
      {
        "select": "SELECT ClassID, BatchID, Section, RoomID FROM dbo.Class",
        "insert": "INSERT INTO Class (ClassID, BatchID, Section, RoomID) VALUES (%s, %s, %s, %s)",
        "update": "UPDATE dbo.Class SET BatchID = %s, Section = %s, RoomID = %s WHERE ClassID = %s",
        "delete": "DELETE FROM dbo.Class WHERE ClassID = %s"
      }
    )

  def student_screen(self):

    self.create_manage_screen(
      "Students", "Student",
      ("StudentID", "Name", "Contact", "ParentContact", "ClassID"),
      [("StudentID", "entry", None), ("Name", "entry", None), ("Contact", "entry", None), ("ParentContact", "entry", None), ("ClassID", "combobox", self.get_class_ids)],
      {
        "select": "SELECT StudentID, Name, Contact, ParentContact, ClassID FROM dbo.Student",
        "insert": "INSERT INTO dbo.Student (StudentID, Name, Contact, ParentContact, ClassID) VALUES (%s, %s, %s, %s, %s)",
        "update": "UPDATE dbo.Student SET Name = %s, Contact = %s, ParentContact = %s, ClassID = %s WHERE StudentID = %s",
        "delete": "DELETE FROM dbo.Student WHERE StudentID = %s"
      }
    )

  def teacher_screen(self):
    
    self.create_manage_screen(
      "Teachers", "Teachers",
      ("TeacherID", "Name", "Subject", "DailySalary"),
      [("TeacherID", "entry", None), ("Name", "entry", None), ("Subject", "entry", None), ("DailySalary", "entry", None)],
      {
        "select": "SELECT TeacherID, Name, Subject, DailySalary FROM dbo.Teacher",
        "insert": "INSERT INTO dbo.Teacher (TeacherID, Name, Subject, DailySalary) VALUES (%s, %s, %s, %s)",
        "update": "UPDATE dbo.Teacher SET Name = %s, Subject = %s, DailySalary = %s WHERE TeacherID = %s",
        "delete": "DELETE FROM dbo.Teacher WHERE TeacherID = %s"
      }
    )

  def timetable_screen(self):
    
    self.create_manage_screen(
      "Timetable", "TimetableEntries",
      ("BatchID", "Day", "Period", "Subject"),
      [("BatchID", "combobox", self.get_batch_ids), ("Day", "combobox", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]), ("Period", "combobox", [1, 2, 3, 4, 5, 6]), ("Subject", "entry", None)],
      {
        "select": "SELECT BatchID, Day, Period, Subject FROM dbo.TimetableEntry",
        "insert": "INSERT INTO dbo.TimetableEntry (BatchID, Day, Period, Subject) VALUES (%s, %s, %s, %s)",
        "update": "UPDATE dbo.TimetableEntry SET Subject = %s WHERE BatchID = %s AND Day = %s AND Period = %s",
        "delete": "DELETE FROM dbo.TimetableEntry WHERE BatchID = %s AND Day = %s AND Period = %s"
      }
    )

  def test_screen(self):
  
    self.create_manage_screen(
      "Tests", "Tests",
      ("TestID", "Subject", "Date", "MaxMarks"),
      [("TestID", "entry", None), ("Subject", "entry", None), ("Date", "entry", None), ("MaxMarks", "entry", None)],
      {
        "select": "SELECT TestID, Subject, Date, MaxMarks FROM dbo.Test",
        "insert": "INSERT INTO dbo.Test (TestID, Subject, Date, MaxMarks) VALUES (%s, %s, %s, %s)",
        "update": "UPDATE dbo.Test SET Subject = %s, Date = %s, MaxMarks = %s WHERE TestID = %s",
        "delete": "DELETE FROM dbo.Test WHERE TestID = %s"
      }
    )

  def attendance_screen(self):
    
    self.create_manage_screen(
      "Attendance", "Attendances",
      ("AttendanceID", "StudentID", "Date", "Status"),
      [("AttendanceID", "entry", None), ("StudentID", "combobox", self.get_student_ids), ("Date", "entry", None), ("Status", "combobox", ["Present", "Absent"])],
      {
        "select": "SELECT AttendanceID, StudentID, Date, Status FROM dbo.Attendance",
        "insert": "INSERT INTO dbo.Attendance (StudentID, Date, Status) VALUES (%s, %s, %s)",
        "update": "UPDATE dbo.Attendance SET StudentID = %s, Date = %s, Status = %s WHERE AttendanceID = %s",
        "delete": "DELETE FROM dbo.Attendance WHERE AttendanceID = %s"
      }
    )
    self.fields["AttendanceID"].config(state='disabled')  # Auto-increment

  def teacher_attendance_screen(self):
    
    self.create_manage_screen(
      "Teacher Attendance", "TeacherAttendances",
      ("AttendanceID", "TeacherID", "Date", "Status"),
      [("AttendanceID", "entry", None), ("TeacherID", "combobox", self.get_teacher_ids), ("Date", "entry", None), ("Status", "combobox", ["Present", "Absent"])],
      {
        "select": "SELECT AttendanceID, TeacherID, Date, Status FROM dbo.TeacherAttendance",
        "insert": "INSERT INTO dbo.TeacherAttendance (TeacherID, Date, Status) VALUES (%s, %s, %s)",
        "update": "UPDATE dbo.TeacherAttendance SET TeacherID = %s, Date = %s, Status = %s WHERE AttendanceID = %s",
        "delete": "DELETE FROM dbo.TeacherAttendance WHERE AttendanceID = %s"
      }
    )
    self.fields["AttendanceID"].config(state='disabled')  # Auto-increment

  def salary_screen(self):
    
    self.create_manage_screen(
      "Salaries", "Salaries",
      ("SalaryID", "TeacherID", "Month", "TotalDaysPresent", "Amount"),
      [("SalaryID", "entry", None), ("TeacherID", "combobox", self.get_teacher_ids), ("Month", "entry", None), ("TotalDaysPresent", "entry", None), ("Amount", "entry", None)],
      {
        "select": "SELECT SalaryID, TeacherID, Month, TotalDaysPresent, Amount FROM dbo.Salary",
        "insert": "INSERT INTO dbo.Salary (TeacherID, Month, TotalDaysPresent, Amount) VALUES (%s, %s, %s, %s)",
        "update": "UPDATE dbo.Salary SET TeacherID = %s, Month = %s, TotalDaysPresent = %s, Amount = %s WHERE SalaryID = %s",
        "delete": "DELETE FROM dbo.Salary WHERE SalaryID = %s"
      }
    )
    self.fields["SalaryID"].config(state='disabled')  # Auto-increment

  def asset_screen(self):
  
    self.create_manage_screen(
      "Classroom Assets", "ClassroomAssets",
      ("AssetID", "RoomID", "Type", "Quantity"),
      [("AssetID", "entry", None), ("RoomID", "combobox", self.get_room_ids), ("Type", "combobox", ["Chair", "AC"]), ("Quantity", "entry", None)],
      {
        "select": "SELECT AssetID, RoomID, Type, Quantity FROM dbo.ClassroomAsset",
        "insert": "INSERT INTO dbo.ClassroomAsset (RoomID, Type, Quantity) VALUES (%s, %s, %s)",
        "update": "UPDATE dbo.ClassroomAsset SET RoomID = %s, Type = %s, Quantity = %s WHERE AssetID = %s",
        "delete": "DELETE FROM dbo.ClassroomAsset WHERE AssetID = %s"
      }
    )
    self.fields["AssetID"].config(state='disabled')  # Auto-increment

  def maintenance_screen(self):
    
    self.create_manage_screen(
      "Maintenance", "Maintenances",
      ("MaintenanceID", "AssetID", "RepairDate", "Cost", "Status"),
      [("MaintenanceID", "entry", None), ("AssetID", "combobox", self.get_asset_ids), ("RepairDate", "entry", None), ("Cost", "entry", None), ("Status", "combobox", ["Pending", "Done"])],
      {
        "select": "SELECT MaintenanceID, AssetID, RepairDate, Cost, Status FROM dbo.Maintenance",
        "insert": "INSERT INTO dbo.Maintenance (AssetID, RepairDate, Cost, Status) VALUES (%s, %s, %s, %s)",
        "update": "UPDATE dbo.Maintenance SET AssetID = %s, RepairDate = %s, Cost = %s, Status = %s WHERE MaintenanceID = %s",
        "delete": "DELETE FROM dbo.Maintenance WHERE MaintenanceID = %s"
      }
    )
    self.fields["MaintenanceID"].config(state='disabled')  # Auto-increment

  def fee_screen(self):
    
    self.create_manage_screen(
      "Fees", "Fees",
      ("FeeID", "StudentID", "Amount", "Discount", "DueDate", "PaidStatus"),
      [("FeeID", "entry", None), ("StudentID", "combobox", self.get_student_ids), ("Amount", "entry", None), ("Discount", "entry", None), ("DueDate", "entry", None), ("PaidStatus", "combobox", ["0", "1"])],
      {
        "select": "SELECT FeeID, StudentID, Amount, Discount, DueDate, PaidStatus FROM dbo.Fee",
        "insert": "INSERT INTO dbo.Fee (StudentID, Amount, Discount, DueDate, PaidStatus) VALUES (%s, %s, %s, %s, %s)",
        "update": "UPDATE dbo.Fee SET StudentID = %s, Amount = %s, Discount = %s, DueDate = %s, PaidStatus = %s WHERE FeeID = %s",
        "delete": "DELETE FROM dbo.Fee WHERE FeeID = %s"
      }
    )
    self.fields["FeeID"].config(state='disabled')  # Auto-increment

  def expense_screen(self):
    
    self.create_manage_screen(
      "Expenses", "Expenses",
      ("ExpenseID", "Type", "Amount", "Date"),
      [("ExpenseID", "entry", None), ("Type", "entry", None), ("Amount", "entry", None), ("Date", "entry", None)],
      {
        "select": "SELECT ExpenseID, Type, Amount, Date FROM dbo.Expense",
        "insert": "INSERT INTO dbo.Expense (Type, Amount, Date) VALUES (%s, %s, %s)",
        "update": "UPDATE dbo.Expense SET Type = %s, Amount = %s, Date = %s WHERE ExpenseID = %s",
        "delete": "DELETE FROM dbo.Expense WHERE ExpenseID = %s"
      }
    )
    self.fields["ExpenseID"].config(state='disabled')  # Auto-increment

if __name__ == "__main__":
  root = ctk.CTk()
  app = ASKAcademyApp(root)
  root.mainloop()
