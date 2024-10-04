import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Load data
df = pd.read_csv(r'updatemood.csv')

# Prepare features and target
X = df.drop(columns=['name', 'album', 'artist', 'id', 'release_date', 'mood'])
y = df['mood']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train SVM model
svm_model = SVC()
svm_model.fit(X_train_scaled, y_train)

# Create GUI window
root = tk.Tk()
root.title("Song Mood and Rating Recommender")
root.geometry('800x500')  # Set size of the window
root.configure(bg="#f0f8ff")  # Light blue background for better look

# Style for treeview
style = ttk.Style()
style.theme_use("clam")  # Modern look
style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

# Function to make predictions based on user input
def predict_mood():
    user_mood = mood_entry.get().strip().lower()
    user_rating = rating_entry.get().strip()
    
    # Clear previous results in treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Validate user rating input
    try:
        user_rating = int(user_rating)
        if user_rating < 1 or user_rating > 5:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid Rating", "Please enter a valid rating between 1 and 5.")
        return

    # Find songs that match the mood and rating
    songs_with_predicted_mood = df[(df['mood'].str.lower() == user_mood) & (df['Rating'] == user_rating)][['name', 'artist', 'album', 'Rating']]

    # Sort the results by rating in descending order
    songs_with_predicted_mood = songs_with_predicted_mood.sort_values(by='Rating', ascending=False)

    if not songs_with_predicted_mood.empty:
        # Show songs in the treeview (table)
        for index, row in songs_with_predicted_mood.iterrows():
            tree.insert('', 'end', values=(row['name'], row['artist'], row['album'], row['Rating']))
        
        # Calculate and display accuracy
        y_pred_svm = svm_model.predict(X_test_scaled)
        svm_accuracy = accuracy_score(y_test, y_pred_svm)
       # print("made by Aditya kushwaha")
        accuracy_label.config(text=f"made by Aditya kushwaha ")
       
    
    else:
        messagebox.showwarning("No Songs Found", f"No songs found with the mood '{user_mood}' and rating '{user_rating}'.")

# Create GUI elements
title_label = tk.Label(root, text="Song Mood and Rating Recommender", font=("Arial", 16, "bold"), bg="#f0f8ff")
title_label.pack(pady=10)

input_frame = tk.Frame(root, bg="#f0f8ff")
input_frame.pack(pady=9)

mood_label = tk.Label(input_frame, text="Enter the mood (e.g., Happy, Angry):", font=("Arial", 12), bg="#f0f8ff")
mood_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

mood_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
mood_entry.grid(row=0, column=1, padx=10, pady=5)

rating_label = tk.Label(input_frame, text="Enter the rating (1 to 5):", font=("Arial", 12), bg="#f0f8ff")
rating_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

rating_entry = tk.Entry(input_frame, font=("Time Square roman", 12), width=20)
rating_entry.grid(row=1, column=1, padx=10, pady=5)

predict_button = tk.Button(root, text="Get Songs", command=predict_mood, font=("Arial", 12), bg="#4682b4", fg="white")
predict_button.pack(pady=10)

# Treeview (table) to display song recommendations
columns = ('Song', 'Artist', 'Album', 'Rating')
tree = ttk.Treeview(root, columns=columns, show='headings', height=8)
tree.heading('Song', text='Song')
tree.heading('Artist', text='Artist')
tree.heading('Album', text='Album')
tree.heading('Rating', text='Rating')
tree.pack(pady=10, padx=20, fill=tk.X)

# Label to display accuracy
accuracy_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f8ff")
accuracy_label.pack(pady=5)

# Run the GUI
root.mainloop()
