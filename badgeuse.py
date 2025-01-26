import tkinter as tk
from tkinter import ttk, messagebox
import csv
from smartcard.System import readers
from smartcard.util import toHexString
import threading
import time

class BadgeuseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Badgeuse - Appel étudiant")
        self.students = []  
        self.running = False
        self.reader_connection = None
        self.current_reader = None
        self.reader_status = tk.StringVar(value="Device : NONE")
        self.reader_color = "red"

        self.student_dict = self.load_student_data()
        self.setup_ui()
        self.check_reader_status()

        self.load_all_students()

    def load_student_data(self):
        student_data = {}
        try:
            with open('etudiants.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    student_data[row['ID']] = row['Nom']
        except FileNotFoundError:
            print("[WARNING] Fichier 'etudiants.csv' non trouvé.")
            messagebox.showwarning("Attention", "Le fichier 'etudiants.csv' n'a pas été trouvé. Les étudiants seront affichés comme 'Nom inconnu'.")
        return student_data

    def setup_ui(self):
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)

        self.status_label = tk.Label(self.status_frame, textvariable=self.reader_status, fg=self.reader_color, font=('Arial', 12, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Nom", "Statut"), show="headings")
        self.tree.heading("ID", text="ID Carte")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Statut", text="Statut")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.start_button = tk.Button(self.root, text="Démarrer Lecture Continue", command=self.start_reading, bg="#4CAF50", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.stop_button = tk.Button(self.root, text="Arrêter Lecture", command=self.stop_reading, state=tk.DISABLED, bg="#f44336", fg="white")
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_to_file, bg="#2196F3", fg="white")
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=10)

        self.fetch_button = tk.Button(self.root, text="Fetch Etudiants", command=self.fetch_students, bg="#FF9800", fg="white")
        self.fetch_button.pack(side=tk.RIGHT, padx=5, pady=10)

    def fetch_students(self):
        self.student_dict = self.load_student_data()
        self.load_all_students()

    def load_all_students(self):
        for uid, name in self.student_dict.items():
            statut = "Absent"
            self.tree.insert("", tk.END, values=(uid, name, statut))

    def connect_reader(self):
        try:
            if not self.current_reader:
                raise Exception("Aucun lecteur NFC détecté.")
            print("[INFO] Connexion au lecteur NFC...")
            connection = self.current_reader.createConnection()
            connection.connect()
            print("[INFO] Connexion au lecteur établie.")
            return connection
        except Exception as e:
            print(f"[ERROR] Impossible de se connecter au lecteur : {e}")
            messagebox.showerror("Erreur", f"Impossible de se connecter au lecteur : {e}")
            return None

    def check_reader_status(self):
        try:
            available_readers = readers()
            if available_readers:
                self.current_reader = available_readers[0]
                self.reader_status.set(f"Device : {self.current_reader}")
                self.reader_color = "green"
            else:
                self.current_reader = None
                self.reader_status.set("Device : NONE")
                self.reader_color = "red"
        except Exception:
            self.current_reader = None
            self.reader_status.set("Device : NONE")
            self.reader_color = "red"

        self.status_label.config(fg=self.reader_color)
        self.root.after(1000, self.check_reader_status)

    def start_reading(self):
        if not self.current_reader:
            messagebox.showerror("Erreur", "Aucun lecteur connecté.")
            return

        self.reader_connection = self.connect_reader()
        if not self.reader_connection:
            return

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        threading.Thread(target=self.reading_loop, daemon=True).start()

    def stop_reading(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reading_loop(self):
        scanned_cards = set()
        while self.running:
            uid = self.read_card(self.reader_connection)
            if uid:
                if uid not in scanned_cards:
                    scanned_cards.add(uid)
                    nom = self.student_dict.get(uid, "Nom inconnu")
                    statut = "Présent"

                    found = False
                    for child in self.tree.get_children():
                        item = self.tree.item(child)
                        if item['values'][0] == uid:
                            self.tree.item(child, values=(uid, nom, statut))
                            found = True
                    if not found:
                        self.tree.insert("", tk.END, values=(uid, nom, statut))

            time.sleep(1)

    def read_card(self, connection):
        try:
            response, sw1, sw2 = connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
            uid = toHexString(response) if response else None
            return uid
        except Exception:
            return None

    def save_to_file(self):
        try:
            with open("presence_etudiants.csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["ID", "Nom", "Statut"])
                writer.writeheader()
                
                items = [self.tree.item(child)['values'] for child in self.tree.get_children()]
                items.sort(key=lambda x: x[2])

                for uid, nom, statut in items:
                    writer.writerow({"ID": uid, "Nom": nom, "Statut": statut})
                
                messagebox.showinfo("Succès", "Les données ont été sauvegardées.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder les données : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BadgeuseApp(root)
    root.mainloop()
