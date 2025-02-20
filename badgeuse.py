import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
from smartcard.System import readers
from smartcard.util import toHexString
import threading
import time
from tkinter import filedialog


class BadgeuseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Badgeuse - Appel étudiant")
        self.students = []
        self.running = False
        self.current_reader = None
        self.reader_status = tk.StringVar(value="Device : NONE")
        self.reader_color = "red"
        self.limit_time = None
        self.student_dict = {}
        self.name_save = None
        self.setup_ui()
        self.check_reader_status()

    def setup_ui(self):
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)

        self.status_label = tk.Label(self.status_frame, textvariable=self.reader_status, fg=self.reader_color, font=('Arial', 12, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.limit_time_button = tk.Button(self.status_frame, text="Set Limit Time", command=self.set_limit_time, bg="#FF9800", fg="white")
        self.limit_time_button.pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "etudiant", "Statut", "Heure de Passage"), show="headings")
        self.tree.heading("ID", text="ID Carte")
        self.tree.heading("etudiant", text="etudiant")
        self.tree.heading("Statut", text="Statut")
        self.tree.heading("Heure de Passage", text="Heure de Passage")
        self.tree.column("ID", anchor=tk.CENTER, stretch=tk.YES)
        self.tree.column("etudiant", anchor=tk.CENTER, stretch=tk.YES)
        self.tree.column("Statut", anchor=tk.CENTER, stretch=tk.YES)
        self.tree.column("Heure de Passage", anchor=tk.CENTER, stretch=tk.YES)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.start_button = tk.Button(self.root, text="Démarrer Lecture Continue", command=self.start_reading, bg="#4CAF50", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.stop_button = tk.Button(self.root, text="Arrêter Lecture", command=self.stop_reading, state=tk.DISABLED, bg="#f44336", fg="white")
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_to_file, bg="#2196F3", fg="white")
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=10)

        self.fetch_button = tk.Button(self.root, text="Fetch Etudiants", command=self.fetch_students, bg="#FF9800", fg="white")
        self.fetch_button.pack(side=tk.RIGHT, padx=5, pady=10)

    def set_limit_time(self):
        self.limit_time = tk.simpledialog.askstring("Set Limit Time", "Enter limit time (HH:MM):")
        if self.limit_time:
            try:
                time.strptime(self.limit_time, "%H:%M")
                messagebox.showinfo("Success", f"Limit time set to {self.limit_time}")
            except ValueError:
                messagebox.showerror("Error", "Invalid time format. Please enter in HH:MM format.")
        else:
            self.limit_time = None

    def fetch_students(self):
        student_data = {}
        for child in self.tree.get_children():
            item = self.tree.item(child)
            if item['values'][2] != "Absent":
                if not messagebox.askyesno("Confirmation", "Cela va supprimer la liste d'étudiants scannés. Êtes-vous sûr ?"):
                    return
            break
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier d'étudiants",
            filetypes=[("Fichiers CSV étudiants", "etudiants_*.csv")]
        )
        file_name = file_path.split("/")[-1]
        self.name_save = "présence_" + file_name
        if file_path:
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        student_data[row['ID']] = row['etudiant']
                messagebox.showinfo("Succès", f"Fichier '{file_path}' chargé avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")
        else:
            return

        self.student_dict = student_data
        self.tree.delete(*self.tree.get_children())
        sorted_students = sorted(self.student_dict.items(), key=lambda x: x[1])
        for uid, name in sorted_students:
            statut = "Absent"
            self.tree.insert("", tk.END, values=(uid, name, statut))

    def connect_reader(self):
        try:
            if self.current_reader:
                connection = self.current_reader.createConnection()
                connection.connect()
                return connection
        except Exception as e:
            print("[INFOS] Recherche de card ...")
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
            connection = self.connect_reader()
            if connection:
                uid = self.read_card(connection)
                if uid and uid not in scanned_cards:
                    scanned_cards.add(uid)
                    etudiant = self.student_dict.get(uid, "etudiant inconnu")
                    current_time = time.strftime("%H:%M")
                    statut = "Présent"

                    if self.limit_time and current_time > self.limit_time:
                            statut = "Retard"

                    found = False
                    for child in self.tree.get_children():
                        item = self.tree.item(child)
                        if item['values'][0] == uid:
                            self.tree.item(child, values=(uid, etudiant, statut, current_time))
                            found = True
                    if not found:
                        self.tree.insert("", tk.END, values=(uid, etudiant, statut, current_time))
                connection.disconnect()
            time.sleep(0.5)

    def read_card(self, connection):
        try:
            response = connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])[0]
            return toHexString(response) if response else None
        except Exception:
            return None

    def save_to_file(self):
        try:
            with open(self.name_save, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["ID", "etudiant", "Statut", "Heure de Passage"])
                writer.writeheader()

                items = [self.tree.item(child)['values'] for child in self.tree.get_children()]
                items.sort(key=lambda x: ("Absent", "Retard", "Présent").index(x[2]))

                for item in items:
                    uid, etudiant, statut = item[:3]
                    heure = item[3] if len(item) > 3 else "N/A"
                    writer.writerow({"ID": uid, "etudiant": etudiant, "Statut": statut, "Heure de Passage": heure})
                messagebox.showinfo("Succès", "Les données ont été sauvegardées.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder les données : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BadgeuseApp(root)
    root.mainloop()
