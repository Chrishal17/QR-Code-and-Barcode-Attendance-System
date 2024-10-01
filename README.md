# QR-Code-and-Barcode-Attendance-System

# QR/Barcode Attendance System

## 1. Overview
This project implements a QR/Barcode Attendance System using Python and Tkinter for the GUI, OpenCV for camera access, Pyzbar for barcode/QR code decoding, and Matplotlib for data visualization.

## 2. Features
1. **Camera Integration:** Opens and closes the camera to scan QR codes and barcodes.
2. **Attendance Tracking:** Records attendance in a CSV file with name, date, and time.
3. **View Attendance:** Displays attendance records in a table format.
4. **Graphical Report:** Visualizes attendance data using a bar graph.
5. **Attendance Reset:** Allows resetting of attendance records.
6. **Time-Limited Attendance:** Stops attendance collection after a specific time.

## 3. Prerequisites
- Python 3.x
- Required libraries:
  ```bash
  pip install opencv-python pillow pyzbar matplotlib
