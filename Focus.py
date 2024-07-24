import tkinter as tk
from datetime import datetime
from tkinter import messagebox

class Focus:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker")

        # Initialize variables to store start times etc
        self.task_start_times = {
            "Sport": None,
            "Lesen": None,
            "Mahlzeit": None,
            "Arbeit": None,
            "Laufen": None,
            "Me-Time": None,
            "Family-Time": None,
            "Tabletten": None
        }

        # Create main frame
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        # Create task buttons
        self.create_task_buttons()

        # Create start and stop buttons for each task
        self.create_control_buttons()

        # Entry for adding new focus
        self.new_focus_frame = tk.Frame(root)
        self.new_focus_frame.pack(pady=10)

        tk.Label(self.new_focus_frame, text="Neuer Fokus:").pack(side='left')
        self.new_focus_entry = tk.Entry(self.new_focus_frame)
        self.new_focus_entry.pack(side='left', padx=5)

        self.focus_type_var = tk.StringVar(value="Lange Zeit")
        tk.Radiobutton(self.new_focus_frame, text="Lange Zeit", variable=self.focus_type_var, value="Lange Zeit").pack(side='left')
        tk.Radiobutton(self.new_focus_frame, text="Kurze Zeit", variable=self.focus_type_var, value="Kurze Zeit").pack(side='left')

        self.add_focus_button = tk.Button(self.new_focus_frame, text="Hinzufügen", command=self.add_new_focus)
        self.add_focus_button.pack(side='left', padx=5)

        # Display log
        self.log = tk.Text(root, state='disabled', width=50, height=10)
        self.log.pack(pady=20)

        # Current task
        self.current_task = None

    def create_task_buttons(self):
        tasks = ["Sport", "Lesen", "Mahlzeit", "Arbeit", "Laufen", "Me-Time", "Family-Time", "Tabletten"]
        self.buttons = {}

        for task in tasks:
            btn = tk.Button(self.frame, text=task, command=lambda t=task: self.track_time(t))
            btn.pack(side='left', padx=5)
            self.buttons[task] = btn

    def create_control_buttons(self):
        self.start_button = tk.Button(self.frame, text="Start", command=self.start_task)
        self.start_button.pack(side='left', padx=5)

        self.stop_button = tk.Button(self.frame, text="Stop", command=self.stop_task)
        self.stop_button.pack(side='left', padx=5)

        self.delete_button = tk.Button(self.frame, text="Löschen", command=self.delete_focus)
        self.delete_button.pack(side='left', padx=5)

    def add_new_focus(self):
        new_focus = self.new_focus_entry.get()
        focus_type = self.focus_type_var.get()

        if new_focus:
            if new_focus in self.task_start_times:
                messagebox.showwarning("Fehler", "Dieser Fokus existiert bereits.")
                return

            self.task_start_times[new_focus] = None
            btn = tk.Button(self.frame, text=new_focus, command=lambda t=new_focus: self.track_time(t))
            btn.pack(side='left', padx=5)
            self.buttons[new_focus] = btn

            if focus_type == "Kurze Zeit":
                self.buttons[new_focus]['command'] = lambda t=new_focus: self.track_time(t, kurze_zeit=True)

            self.log_task(f"Neuer Fokus hinzugefügt: {new_focus} ({focus_type})")
            self.new_focus_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Fehler", "Bitte geben Sie einen Namen für den neuen Fokus ein.")

    def delete_focus(self):
        focus_to_delete = self.new_focus_entry.get()
        if focus_to_delete in self.task_start_times:
            confirm = messagebox.askyesno("Bestätigung", f"Möchten Sie den Fokus '{focus_to_delete}' wirklich löschen?")
            if confirm:
                self.task_start_times.pop(focus_to_delete)
                self.buttons[focus_to_delete].destroy()
                self.buttons.pop(focus_to_delete)
                self.log_task(f"Fokus '{focus_to_delete}' wurde gelöscht.")
                self.new_focus_entry.delete(0, 'end')
            else:
                messagebox.showinfo("Abgebrochen", "Löschen abgebrochen.")
        else:
            messagebox.showwarning("Fehler", "Fokus nicht gefunden.")

    def track_time(self, task, kurze_zeit=False):
        if kurze_zeit:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_task(f"{task} um {current_time}")
        else:
            self.current_task = task
            messagebox.showinfo("Task ausgewählt", f"{task} gestartet. Bitte Start drücken.")

    def start_task(self):
        if self.current_task:
            self.task_start_times[self.current_task] = datetime.now()
            self.log_task(f"{self.current_task} gestartet um {self.task_start_times[self.current_task].strftime('%Y-%m-%d %H:%M:%S')}")

    def stop_task(self):
        if self.current_task and self.task_start_times[self.current_task]:
            end_time = datetime.now()
            duration = end_time - self.task_start_times[self.current_task]
            self.log_task(f"{self.current_task} gestoppt um {end_time.strftime('%Y-%m-%d %H:%M:%S')}. Dauer: {duration}")
            self.task_start_times[self.current_task] = None

    def log_task(self, message):
        self.log.configure(state='normal')
        self.log.insert('end', message + "\n")
        self.log.configure(state='disabled')
        self.log.yview('end')

if __name__ == "__main__":
    root = tk.Tk()
    app = Focus(root)
    root.mainloop()
