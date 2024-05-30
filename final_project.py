import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

class Member:
    def __init__(self, member_id, name, age, contact, purpose, attendance=None, password=None):
        self.member_id = member_id
        self.name = name
        self.age = age
        self.contact = contact
        self.purpose = purpose
        self.attendance = attendance if attendance else {}
        self.password = password

    def mark_attendance(self, date, entry_time, exit_time=None):
        if date not in self.attendance:
            self.attendance[date] = []
        self.attendance[date].append({"entry": entry_time, "exit": exit_time})

    def get_attendance(self):
        return self.attendance

    def __str__(self):
        return f"{self.name} (ID: {self.member_id}, Age: {self.age}, Contact: {self.contact}, Purpose: {self.purpose})"

class GymManagementSystem:
    def __init__(self):
        self.members = []
        self.load_data()

    def register_member(self, name, age, contact, purpose):
        member_id = len(self.members) + 1  # Assign a unique ID
        password = simpledialog.askstring("Create Password", "Create a password for login:")
        member = Member(member_id, name, age, contact, purpose, password=password)
        self.members.append(member)
        self.save_data()
        messagebox.showinfo("Registration Successful", f"Registration successful!\nMember ID: {member.member_id}\nPassword: {member.password}")
        return member

    def login_member(self, member_id, password):
        for member in self.members:
            if member.member_id == member_id and member.password == password:
                return member
        return None

    def check_in(self, member):
        date = datetime.now().strftime("%Y-%m-%d")
        entry_time = datetime.now().strftime("%H:%M:%S")
        self.mark_member_attendance(member, date, entry_time)
        messagebox.showinfo("Check-in Successful", "Check-in successful!")

    def check_out(self, member):
        date = datetime.now().strftime("%Y-%m-%d")
        exit_time = datetime.now().strftime("%H:%M:%S")
        attendance = member.get_attendance()
        if date in attendance and attendance[date][-1]["exit"] is None:
            attendance[date][-1]["exit"] = exit_time
            self.save_data()
            messagebox.showinfo("Check-out Successful", "Check-out successful!")
        else:
            messagebox.showerror("Check-out Error", "Check-in record not found or already checked out.")

    def get_workout_plan(self, member):
        workout_plan = ""
        purpose = member.purpose.lower()
        if purpose == "strength building":
            workout_plan = "Bro Split:\nMonday: Chest (Bench Press, Incline Dumbbell Press, Dumbbell Flyes, Push-Ups)\nTuesday: Back (Deadlifts, Pull-Ups, Bent Over Rows, Lat Pulldowns)\nWednesday: Rest\nThursday: Shoulders (Military Press, Lateral Raises, Front Raises, Shrugs)\nFriday: Arms (Barbell Curls, Tricep Dips, Hammer Curls, Skull Crushers)"
        elif purpose == "weight loss":
            workout_plan = "Cardio + Bro Split:\nMonday: Cardio (30 minutes)\nTuesday: Chest & Triceps (Bench Press, Tricep Dips, Incline Dumbbell Press, Tricep Pushdowns)\nWednesday: Back & Biceps (Deadlifts, Barbell Rows, Pull-Ups, Barbell Curls)\nThursday: Cardio (30 minutes)\nFriday: Legs & Shoulders (Squats, Lunges, Shoulder Press, Lateral Raises)"
        elif purpose == "muscle gain":
            workout_plan = "Push Pull Legs:\nMonday (Push): Chest (Bench Press, Incline Dumbbell Press, Dumbbell Flyes), Shoulders (Military Press, Lateral Raises), Triceps (Tricep Dips, Skull Crushers)\nTuesday (Pull): Back (Deadlifts, Pull-Ups, Bent Over Rows), Biceps (Barbell Curls, Hammer Curls)\nWednesday (Legs): Quads (Squats, Leg Press), Hamstrings (Deadlifts, Romanian Deadlifts), Calves (Calf Raises)"
        return workout_plan

    def mark_member_attendance(self, member, date, entry_time, exit_time=None):
        member.mark_attendance(date, entry_time, exit_time)

    def get_member_attendance(self, member):
        return member.get_attendance()

    def save_data(self):
        data = {"members": [vars(member) for member in self.members]}
        try:
            with open("gym_data.json", "w") as file:
                json.dump(data, file)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data: {e}")

    def load_data(self):
        try:
            with open("gym_data.json", "r") as file:
                data = json.load(file)
                self.members = [Member(**member_data) for member_data in data["members"]]
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            messagebox.showerror("Load Error", "Failed to decode JSON data.")
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading data: {e}")
    def delete_member(self, member):
        confirmation = messagebox.askyesno("Delete Member", f"Are you sure you want to delete {member.name}?")
        if confirmation:
            self.members.remove(member)
            self.save_data()
            messagebox.showinfo("Member Deleted", f"{member.name} has been successfully deleted.")


# GUI functions

def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Register New Member")

    tk.Label(registration_window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(registration_window)
    name_entry.grid(row=0, column=1)

    tk.Label(registration_window, text="Age:").grid(row=1, column=0)
    age_entry = tk.Entry(registration_window)
    age_entry.grid(row=1, column=1)

    tk.Label(registration_window, text="Contact:").grid(row=2, column=0)
    contact_entry = tk.Entry(registration_window)
    contact_entry.grid(row=2, column=1)

    tk.Label(registration_window, text="Purpose of Joining:").grid(row=3, column=0)
    purpose_var = tk.StringVar(registration_window)
    purpose_var.set("Strength building")
    purpose_optionmenu = tk.OptionMenu(registration_window, purpose_var, "Strength building", "Weight loss", "Muscle gain")
    purpose_optionmenu.grid(row=3, column=1)

    def register_member():
        name = name_entry.get()
        age = int(age_entry.get())
        contact = contact_entry.get()
        purpose = purpose_var.get()

        member = gym_system.register_member(name, age, contact, purpose)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)

    register_button = tk.Button(registration_window, text="Register", command=register_member)
    register_button.grid(row=4, columnspan=2, pady=10)

def open_login_window():
    def login():
        member_id = member_id_entry.get()
        password = password_entry.get()

        if member_id == 'admin' and password == 'admin':  # Check if login is for admin
            open_admin_window()
        else:
            try:
                member_id = int(member_id)
                member = gym_system.login_member(member_id, password)
                if member:
                    login_window.destroy()
                    open_member_window(member)
                else:
                    messagebox.showerror("Login Error", "Invalid ID or password.")
            except ValueError:
                messagebox.showerror("Login Error", "Invalid ID. Please enter a valid member ID.")

    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Member ID:").grid(row=0, column=0)
    member_id_entry = tk.Entry(login_window)
    member_id_entry.grid(row=0, column=1)

    tk.Label(login_window, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.grid(row=2, columnspan=2, pady=10)

def open_admin_window():
    def search_member():
        search_query = search_entry.get().lower()
        for widget in results_frame.winfo_children():
            widget.destroy()
        for member in gym_system.members:
            if search_query in member.name.lower():
                display_member_info(member, results_frame)
    
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")

    tk.Label(admin_window, text="Member Details", font=("Helvetica", 16)).pack()

    search_frame = tk.Frame(admin_window)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search by Name:").pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_button = tk.Button(search_frame, text="Search", command=search_member)
    search_button.pack(side=tk.LEFT)

    results_frame = tk.Frame(admin_window)
    results_frame.pack(pady=10)

    for member in gym_system.members:
        display_member_info(member, results_frame)

def display_member_info(member, parent_frame):
    member_frame = tk.Frame(parent_frame, borderwidth=2, relief="groove")
    member_frame.pack(pady=5, fill="x")

    member_info_frame = tk.Frame(member_frame)
    member_info_frame.pack(side=tk.LEFT, fill="x", expand=True)

    tk.Label(member_info_frame, text=f"Name: {member.name}").grid(row=0, column=0, sticky="w")
    tk.Label(member_info_frame, text=f"ID: {member.member_id}").grid(row=0, column=1, sticky="w")
    tk.Label(member_info_frame, text=f"Age: {member.age}").grid(row=1, column=0, sticky="w")
    tk.Label(member_info_frame, text=f"Contact: {member.contact}").grid(row=1, column=1, sticky="w")
    tk.Label(member_info_frame, text=f"Purpose: {member.purpose}").grid(row=2, column=0, columnspan=2, sticky="w")
    tk.Label(member_info_frame, text=f"Password: {member.password}").grid(row=3, column=0, columnspan=2, sticky="w")

    attendance_button = tk.Button(member_frame, text="View Attendance", command=lambda: open_attendance_window(member))
    attendance_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    edit_button = tk.Button(member_frame, text="Edit Details", command=lambda: open_edit_window(member))
    edit_button.pack(side=tk.RIGHT, padx=5, pady=5)
    delete_button = tk.Button(member_frame, text="Delete", command=lambda: gym_system.delete_member(member))
    delete_button.pack(side=tk.RIGHT, padx=5, pady=5)



def open_edit_window(member):
    def save_changes():
        member.name = name_entry.get()
        member.age = int(age_entry.get())
        member.contact = contact_entry.get()
        member.purpose = purpose_var.get()
        member.password = password_entry.get()
        gym_system.save_data()
        edit_window.destroy()
        messagebox.showinfo("Edit Successful", "Member details updated successfully!")

    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit Details for {member.name}")

    tk.Label(edit_window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(edit_window)
    name_entry.grid(row=0, column=1)
    name_entry.insert(0, member.name)

    tk.Label(edit_window, text="Age:").grid(row=1, column=0)
    age_entry = tk.Entry(edit_window)
    age_entry.grid(row=1, column=1)
    age_entry.insert(0, member.age)

    tk.Label(edit_window, text="Contact:").grid(row=2, column=0)
    contact_entry = tk.Entry(edit_window)
    contact_entry.grid(row=2, column=1)
    contact_entry.insert(0, member.contact)

    tk.Label(edit_window, text="Purpose of Joining:").grid(row=3, column=0)
    purpose_var = tk.StringVar(edit_window)
    purpose_var.set(member.purpose)
    purpose_optionmenu = tk.OptionMenu(edit_window, purpose_var, "Strength building", "Weight loss", "Muscle gain")
    purpose_optionmenu.grid(row=3, column=1)

    tk.Label(edit_window, text="Password:").grid(row=4, column=0)
    password_entry = tk.Entry(edit_window, show="*")
    password_entry.grid(row=4, column=1)
    password_entry.insert(0, member.password)

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=5, columnspan=2, pady=10)

def open_member_window(member):
    member_window = tk.Toplevel(root)
    member_window.title(f"Welcome, {member.name}")

    tk.Label(member_window, text=f"Welcome, {member.name}!", font=("Helvetica", 16)).pack(pady=10)

    def check_in():
        gym_system.check_in(member)

    def check_out():
        gym_system.check_out(member)

    def view_workout_plan():
        workout_plan = gym_system.get_workout_plan(member)
        messagebox.showinfo("Workout Plan", workout_plan)

    tk.Button(member_window, text="Check-in", command=check_in).pack(pady=5)
    tk.Button(member_window, text="Check-out", command=check_out).pack(pady=5)
    tk.Button(member_window, text="View Workout Plan", command=view_workout_plan).pack(pady=5)
    tk.Button(member_window, text="View Attendance", command=lambda: open_attendance_window(member)).pack(pady=5)

def open_attendance_window(member):
    attendance_window = tk.Toplevel(root)
    attendance_window.title(f"Attendance for {member.name}")

    tk.Label(attendance_window, text=f"Attendance for {member.name}", font=("Helvetica", 16)).pack(pady=10)

    attendance = gym_system.get_member_attendance(member)
    for date, records in attendance.items():
        date_frame = tk.Frame(attendance_window)
        date_frame.pack(pady=5)
        tk.Label(date_frame, text=f"Date: {date}", font=("Helvetica", 12, "bold")).pack()
        for record in records:
            entry_time = record["entry"]
            exit_time = record["exit"] if record["exit"] else "N/A"
            tk.Label(date_frame, text=f"Entry: {entry_time}, Exit: {exit_time}").pack()

# Main application window
root = tk.Tk()
root.title("Gym Management System")

gym_system = GymManagementSystem()

tk.Label(root, text="Welcome to Gym Management System", font=("Helvetica", 18)).pack(pady=10)

tk.Button(root, text="Register New Member", command=open_registration_window).pack(pady=5)
tk.Button(root, text="Login", command=open_login_window).pack(pady=5)

root.mainloop()
