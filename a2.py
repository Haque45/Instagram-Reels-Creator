import os
import sqlite3
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, Toplevel, Listbox, Scrollbar, Frame
from moviepy.video.io.VideoFileClip import VideoFileClip

# Global variable to store the destination folder
destination_folder = ""

# Function to split video
def split_video(video_path, duration):
    if not os.path.exists(video_path):
        messagebox.showerror("Error", "Video file does not exist.")
        return

    if not destination_folder:
        messagebox.showerror("Error", "Please select a destination folder.")
        return

    video = VideoFileClip(video_path)
    video_duration = int(video.duration)
    clips = []

    for start in range(0, video_duration, duration):
        end = min(start + duration, video_duration)
        clip = video.subclipped(start, end)
        clip_filename = os.path.join(destination_folder, f"clip_{start}_{end}.mp4")
        clip.write_videofile(clip_filename, codec="libx264")
        clips.append((video_path, clip_filename, start, end))

    video.close()
    return clips

# Function to save metadata to SQLite database
def save_to_db(clips):
    conn = sqlite3.connect('video_clips.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clips (
            id INTEGER PRIMARY KEY,
            original_filename TEXT,
            clip_filename TEXT,
            start_time INTEGER,
            end_time INTEGER
        )
    ''')
    
    for clip in clips:
        cursor.execute('INSERT INTO clips (original_filename, clip_filename, start_time, end_time) VALUES (?, ?, ?, ?)', clip)

    conn.commit()
    conn.close()

# Function to handle the split video button click
def on_split_video():
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if not video_path:
        return

    try:
        duration = int(duration_entry.get())
        clips = split_video(video_path, duration)
        if clips:
            save_to_db(clips)
            messagebox.showinfo("Success", "Video split successfully and metadata saved to database.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid duration in seconds.")

# Function to show history of split files
def show_history():
    history_window = Toplevel(root)
    history_window.title("History of Split Files")
    history_window.geometry("600x400")
    history_window.configure(bg="#f0f8ff")

    Label(history_window, text="History of Split Files", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#333").pack(pady=10)

    listbox_frame = Frame(history_window)
    listbox_frame.pack(fill="both", expand=True, padx=20, pady=10)

    listbox = Listbox(listbox_frame, width=70, height=15, font=("Courier", 10))
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(listbox_frame)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect('video_clips.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_filename, clip_filename, start_time, end_time FROM clips')
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        listbox.insert("end", f"Original: {row[0]} | Clip: {row[1]} | Start: {row[2]}s | End: {row[3]}s")

# Function to select destination folder
def select_destination_folder():
    global destination_folder
    destination_folder = filedialog.askdirectory(title="Select Destination Folder")
    if destination_folder:
        messagebox.showinfo("Selected Folder", f"Destination folder set to: {destination_folder}")

# Create the GUI
root = Tk()
root.title("Video Splitter")
root.geometry("400x400")
root.configure(bg="#f0f8ff")

Label(root, text="Video Splitter", font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="#333").pack(pady=10)

Label(root, text="Enter Clip Duration (seconds):", font=("Arial", 12), bg="#f0f8ff", fg="#333").pack(pady=5)
duration_entry = Entry(root, font=("Arial", 12), width=15, justify="center")
duration_entry.pack(pady=5)

Button(root, text="Select Destination Folder", font=("Arial", 12), bg="#4682b4", fg="white", command=select_destination_folder).pack(pady=10)
Button(root, text="Split Video", font=("Arial", 12, "bold"), bg="#5cb85c", fg="white", command=on_split_video).pack(pady=10)
Button(root, text="Show History", font=("Arial", 12), bg="#0275d8", fg="white", command=show_history).pack(pady=10)

root.mainloop()
