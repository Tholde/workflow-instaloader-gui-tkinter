import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import instaloader

# Création de l'instance globale d'Instaloader
L = instaloader.Instaloader()


# Fonction pour afficher un message dans la zone de log
def log(msg):
    log_text.configure(state="normal")
    log_text.insert("end", msg + "\n")
    log_text.configure(state="disabled")
    log_text.see("end")


# Ouvre une boîte de dialogue pour choisir un dossier
def choose_dir():
    path = filedialog.askdirectory()
    if path:
        dir_var.set(path)


# Fonction de connexion à Instagram
def login_instagram():
    username = str(username_var.get().strip())
    password = str(password_var.get().strip())
    print("username: " + username)
    print("password: " + password)
    if not username or not password:
        messagebox.showwarning("Champs manquants", "Veuillez entrer votre nom d'utilisateur et mot de passe.")
        return False
    try:
        L.login(username, password)
        log(f"Connecté à Instagram en tant que @{username}")
        return True
    except Exception as e:
        messagebox.showerror("Erreur de connexion", f"❌ Échec de connexion : {e}")
        return False


# Fonction appelée quand l'utilisateur clique sur "Télécharger"
def download():
    # Récupération du hashtag (sans le symbole #)
    hashtag_name = hashtag_var.get().strip().lstrip("#")
    print(f"Hashtag: {hashtag_name}")
    if not hashtag_name:
        messagebox.showwarning("Erreur de saisie", "Veuillez entrer un hashtag.")
        return
    # Vérification du nombre de posts à télécharger
    try:
        max_posts = int(max_var.get()) if max_var.get() else None
    except ValueError:
        messagebox.showerror("Erreur de saisie", "Le nombre de posts doit être un chiffre.")
        return
    # Création du dossier de destination si non spécifié
    directory = dir_var.get() or os.path.join(os.getcwd(), "downloads")
    os.makedirs(directory, exist_ok=True)
    # Connexion obligatoire à Instagram
    if not login_instagram():
        return

    # Fonction de téléchargement à exécuter dans un thread
    def worker():
        log(f"Téléchargement : #{hashtag_name} vers {directory}")
        # Définir le dossier de téléchargement pour Instaloader
        L.dirname_pattern = os.path.join(directory, "{target}")
        try:
            # Chargement des données du hashtag
            hashtag = instaloader.Hashtag.from_name(L.context, hashtag_name)
        except Exception as e:
            log(f"Erreur de récupération du hashtag : {e.message}")
            return
        count = 0
        # Parcours des posts liés au hashtag
        for post in hashtag.get_posts():
            if max_posts and count >= max_posts:
                break
            try:
                # Téléchargement du post
                L.download_post(post, target=f"#{hashtag_name}")
                log(f"{post.shortcode}")
                count += 1
            except Exception as e:
                log(f"{post.shortcode} – {e}")
        log("Téléchargement terminé.")

    # Lancer le téléchargement dans un thread séparé pour ne pas bloquer l'interface
    threading.Thread(target=worker, daemon=True).start()


root = tk.Tk()
root.title("Instaloader GUI – Téléchargement par Hashtag")
root.geometry("550x500")

main = ttk.Frame(root, padding=10)
main.pack(fill="both", expand=True)

# Champs pour les identifiants Instagram
ttk.Label(main, text="Nom d'utilisateur Instagram :").grid(column=0, row=0, sticky="w")
username_var = tk.StringVar()
ttk.Entry(main, textvariable=username_var, width=30).grid(column=1, row=0, sticky="ew")

ttk.Label(main, text="Mot de passe :").grid(column=0, row=1, sticky="w")
password_var = tk.StringVar()
ttk.Entry(main, textvariable=password_var, width=30, show="*").grid(column=1, row=1, sticky="ew")

# Hashtag à rechercher
ttk.Label(main, text="Hashtag (sans #) :").grid(column=0, row=2, sticky="w")
hashtag_var = tk.StringVar(value="hairstylistantwerp")
# hashtag_var = tk.StringVar()
ttk.Entry(main, textvariable=hashtag_var, width=30).grid(column=1, row=2, sticky="ew")

# Nombre de posts à télécharger
ttk.Label(main, text="Max posts (vide = tous) :").grid(column=0, row=3, sticky="w")
max_var = tk.StringVar()
ttk.Entry(main, textvariable=max_var, width=10).grid(column=1, row=3, sticky="w")

# Sélection du dossier de destination
ttk.Label(main, text="Dossier de téléchargement :").grid(column=0, row=4, sticky="w")
dir_var = tk.StringVar()
ttk.Entry(main, textvariable=dir_var, width=30).grid(column=1, row=4, sticky="ew")
ttk.Button(main, text="Choisir…", command=choose_dir).grid(column=2, row=4, padx=5)

# Bouton principal pour lancer le téléchargement
ttk.Button(main, text="Télécharger", command=download).grid(column=0, row=5, columnspan=3, pady=10)

# Zone de logs (readonly)
log_text = tk.Text(main, height=15, state="disabled")
log_text.grid(column=0, row=6, columnspan=3, sticky="nsew", pady=(10, 0))

# Configuration du layout pour que la zone de log prenne l'espace restant
main.columnconfigure(1, weight=1)
main.rowconfigure(6, weight=1)

# Lancement de la boucle principale Tkinter
root.mainloop()
