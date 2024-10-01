import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk
import csv
import time
import os
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode  # Import for barcode scanning
import winsound  # Import for beep sound (Windows only)
from datetime import datetime

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR/Barcode Attendance System")
        self.root.geometry("1280x720")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load and set the background image
        self.bg_image = Image.open("C:/Users/ADMIN/OneDrive/Desktop/students.jpeg")  # Replace with your image path
        self.bg_image = self.bg_image.resize((1280, 720))  # Resize to fit the window
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Background label
        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Load and set the logo image
        self.logo_image = Image.open("C:/Users/ADMIN/OneDrive/Desktop/Hal.jpg")  # Replace with your logo image path
        self.logo_image = self.logo_image.resize((200, 100))  # Resize logo if necessary
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Logo label
        self.logo_label = tk.Label(self.root, image=self.logo_photo, bg="#e6ffe6")
        self.logo_label.place(x=10, y=10)  # Position the logo at the top left

        self.camera_active = False
        self.cap = None
        self.attendance_file = "attendance.csv"
        
        # End time for attendance (set to a specific time)
        self.end_time = datetime(2024, 9, 28, 14, 36, 0)  # Set the time limit (e.g., 6:00 PM on Sep 28, 2024)

        # Title label
        title_label = tk.Label(self.root, text="Attendance System", font=("Arial", 30, "bold"), bg="#e6ffe6", fg="#333")
        title_label.pack(pady=20)

        # Buttons
        button_style = {"font": ("Arial", 16), "width": 20}

        open_camera_btn = tk.Button(self.root, text="Open Camera", command=self.open_camera, **button_style)
        open_camera_btn.pack(pady=10)

        close_camera_btn = tk.Button(self.root, text="Close Camera", command=self.close_camera, **button_style)
        close_camera_btn.pack(pady=10)

        view_attendance_btn = tk.Button(self.root, text="View Attendance", command=self.view_attendance, **button_style)
        view_attendance_btn.pack(pady=10)

        # Reset button to reset the attendance
        reset_btn = tk.Button(self.root, text="Reset Attendance", command=self.reset_attendance, font=("Arial", 16), width=20, bg='red')
        reset_btn.pack(pady=10)

        # Bar Graph Button
        view_graph_btn = tk.Button(self.root, text="View Attendance Graph", command=self.show_attendance_graph, **button_style)
        view_graph_btn.pack(pady=10)

        # Video frame to display camera
        self.video_frame = tk.Label(self.root)
        self.video_frame.pack(pady=20)

        # Time label
        self.time_label = tk.Label(self.root, font=("Arial", 16), bg="#e6ffe6", fg="#333")
        self.time_label.place(x=1100, y=10)

        self.update_time()

    def reset_attendance(self):
        # Reset the attendance by clearing the file but keeping the column headers.
        with open(self.attendance_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Rewrite the column headers, but remove the data
            writer.writerow(["Name", "Date", "Time"])
        messagebox.showinfo("Reset", "Attendance has been reset!")

    def on_closing(self):
        self.root.destroy()

    def open_camera(self):
        if not self.camera_active:
            self.camera_active = True
            self.cap = cv2.VideoCapture(0)
            self.scan_code()

    def close_camera(self):
        if self.camera_active:
            self.camera_active = False
            if self.cap:
                self.cap.release()
            self.video_frame.config(image='')

    def scan_code(self):
        if self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect QR Code
                detector = cv2.QRCodeDetector()
                retval, decoded_info, points, _ = detector.detectAndDecodeMulti(gray_frame)

                # Detect Barcode
                barcodes = decode(frame)

                if retval and decoded_info:
                    for info in decoded_info:
                        if info:
                            self.mark_attendance(info)
                            cv2.putText(frame, "QR Scanned: " + info, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                for barcode in barcodes:
                    barcode_data = barcode.data.decode('utf-8')
                    if barcode_data:
                        self.mark_attendance(barcode_data)
                        cv2.putText(frame, "Barcode Scanned: " + barcode_data, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                # Show the frame in the Tkinter window
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_frame.imgtk = imgtk
                self.video_frame.config(image=imgtk)

            # Check if the current time exceeds the end time for attendance
            if datetime.now() > self.end_time:
                self.close_camera()
                messagebox.showinfo("Time Out", "Attendance time limit exceeded!")
            else:
                self.root.after(10, self.scan_code)

    def mark_attendance(self, Name):
        current_date = time.strftime("%Y-%m-%d")
        current_time = time.strftime("%H:%M:%S")
        with open(self.attendance_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([Name, current_date, current_time])
        winsound.Beep(1000, 500)  # Beep sound (frequency: 1000Hz, duration: 500ms)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def view_attendance(self):
        if os.path.exists(self.attendance_file):
            window = tk.Toplevel(self.root)
            window.title("Attendance Records")
            window.geometry("600x400")

            table = ttk.Treeview(window, columns=("Name", "Date", "Time"), show='headings')
            table.heading("Name", text="Name")
            table.heading("Date", text="Date")
            table.heading("Time", text="Time")
            table.pack(fill=tk.BOTH, expand=True)

            with open(self.attendance_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    table.insert("", tk.END, values=row)
        else:
            messagebox.showerror("Error", "Attendance file not found!")

    def show_attendance_graph(self):
        import matplotlib.pyplot as plt
        from collections import defaultdict
        from datetime import datetime

        # Dictionary to store attendance counts by date
        attendance_by_date = defaultdict(int)

        # Check if attendance file exists
        if os.path.exists(self.attendance_file):
            with open(self.attendance_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row

                # Collect attendance counts by date
                for row in reader:
                    date_str = row[1]  # Date is in the second column (index 1)
                    attendance_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    attendance_by_date[attendance_date] += 1  # Increment attendance count for the date

            if attendance_by_date:
                # Convert dates and counts for plotting
                dates = sorted(attendance_by_date.keys())
                counts = [attendance_by_date[date] for date in dates]

                # Plotting bar chart
                plt.bar(dates, counts)
                plt.xlabel('Date')
                plt.ylabel('Attendance Count (1 unit)')
                plt.title('Attendance Report')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            else:
                messagebox.showinfo("No Attendance", "No attendance data available for graph.")
        else:
            messagebox.showerror("Error", "Attendance file not found!")


if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
