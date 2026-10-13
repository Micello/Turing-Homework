import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path

class Persona:
    def __init__(self, nome, cognome, indirizzo, telefono, eta):
        self.nome = nome
        self.cognome = cognome
        self.indirizzo = indirizzo
        self.telefono = telefono
        self.eta = eta

class Utente:
    def __init__(self, username, password):
        self.username = username
        self.password = password

persone = []
utenti = [Utente("admin", "admin")]

# Lettura e scrittura del file
def carica_persone():
    try:
        with open("informazioni.txt", "r", encoding="utf-8") as file:
            for riga in file:
                riga = riga.strip()

                if not riga:
                    continue

                nome, cognome, indirizzo, telefono, eta = riga.split(";")
                persona = Persona(nome, cognome, indirizzo, telefono, eta)
                persone.append(persona)
    except FileNotFoundError:
        pass


def salva_su_file():
    with open("informazioni.txt", "w", encoding="utf-8") as file:
        for persona in persone:
            file.write(
                f"{persona.nome};{persona.cognome};"
                f"{persona.indirizzo};{persona.telefono};{persona.eta}\n"
            )


# Aggiornamento delle righe visualizzate
def aggiorna_tabella():
    for riga in tabella.get_children():
        tabella.delete(riga)

    for persona in persone:
        tabella.insert(
            "", "end",
            values=(persona.nome, persona.cognome, persona.telefono)
        )


# Finestra per creare o modificare una persona
def editor_persona(persona=None):
    editor = tk.Toplevel(finestra)
    editor.title("Editor-persona")
    editor.columnconfigure(1, weight=1)

    entries = {}

    if persona is None:
        valori = {
            "nome": "",
            "cognome": "",
            "indirizzo": "",
            "telefono": "",
            "eta": ""
        }
    else:
        valori = vars(persona)
    for i, (nome, valore) in enumerate(valori.items()):
        label = tk.Label(editor, text=nome)
        label.grid(row=i+1, column=0)

        entry = tk.Entry(editor)
        entry.grid(row=i+1, column=1, sticky="ew")
        entry.insert(0, str(valore))
        entries[nome] = entry

    def salva(event=None):
        if persona is None:
            nuova_persona = Persona(
                entries["nome"].get(),
                entries["cognome"].get(),
                entries["indirizzo"].get(),
                entries["telefono"].get(),
                entries["eta"].get()
            )

            persone.append(nuova_persona)
        else:
            persona.nome = entries["nome"].get()
            persona.cognome = entries["cognome"].get()
            persona.indirizzo = entries["indirizzo"].get()
            persona.telefono = entries["telefono"].get()
            persona.eta = entries["eta"].get()

        salva_su_file()
        aggiorna_tabella()
        editor.destroy()

    frame_bottoni_editor = tk.Frame(editor)
    frame_bottoni_editor.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

    tk.Button(
        frame_bottoni_editor, text="Salva", image=icone["salva"],
        compound="left", command=salva
    ).pack(side="left", padx=5)
    tk.Button(
        frame_bottoni_editor, text="Annulla", image=icone["annulla"],
        compound="left", command=editor.destroy
    ).pack(side="left", padx=5)


# Azioni dei bottoni principali
def modifica_persona():
    selezione = tabella.selection()

    if not selezione:
        messagebox.showwarning("Nessuna persona selezionata","Selezionare una persona prima di premere Modifica")
        return
    
    riga_selezionata = selezione[0]
    indice = tabella.index(riga_selezionata)
    persona = persone[indice]
    editor_persona(persona)


def elimina_persona():
    selezione = tabella.selection()

    if not selezione:
        messagebox.showwarning("Nessuna persona selezionata", "Per eliminare, è necessario prima selezionare una persona.")
        return

    # nota: funziona perchè nel programma la tabella e persone hanno lo stesso ordine.
    riga_selezionata = selezione[0]
    indice = tabella.index(riga_selezionata)
    persona = persone[indice]

    conferma = messagebox.askyesno("Conferma",f'Eliminare la persona "{persona.nome} {persona.cognome}"?')
    if conferma:
        persone.pop(indice)
        salva_su_file()
        aggiorna_tabella()

def mostra_login():
    login = tk.Toplevel(finestra)
    login.title("Login")

    tk.Label(login, text="Utente").grid(row=0, column=0)
    entry_username = tk.Entry(login)
    entry_username.grid(row=0, column=1)

    tk.Label(login, text="Password").grid(row=1, column=0)
    entry_password = tk.Entry(login, show="*")
    entry_password.grid(row=1, column=1)

    def verifica_login():
        username = entry_username.get()
        password = entry_password.get()

        for utente in utenti:
            if username == utente.username and password == utente.password:
                login.destroy()
                finestra.deiconify()
                return

        messagebox.showerror(
            "Login errato",
            "Username o password non corretti.",
            parent=login
        )

    tk.Button(login, text="LOGIN", command=verifica_login).grid(
        row=2, column=0, columnspan=2
    )

    login.protocol("WM_DELETE_WINDOW", finestra.destroy)
    entry_username.focus_set()
    
# Finestra principale
finestra = tk.Tk()
finestra.withdraw()
finestra.title("Rubrica di Turing")
finestra.geometry("600x400")

# Le immagini restano in memoria e vengono caricate dalla cartella del programma.
cartella_icone = Path(__file__).resolve().parent / "icone"
icone = {}
for nome in ("nuovo", "modifica", "elimina", "salva", "annulla"):
    icone[nome] = tk.PhotoImage(
        master=finestra, file=str(cartella_icone / f"{nome}.png")
    )

# Creazione tabella con Treeview
tabella = ttk.Treeview(
    finestra,
    columns=("nome", "cognome", "telefono"),
    show="headings"
)

tabella.heading("nome", text="Nome")
tabella.heading("cognome", text="Cognome")
tabella.heading("telefono", text="Telefono")

# Creazione dei bottoni (pack tabella successivo al frame per dare spazio ai bottoni)
frame_bottoni = tk.Frame(finestra)
frame_bottoni.pack(side="top", fill="x", padx =5, pady=5)
tabella.pack(fill="both", expand=True)

btn_nuovo = tk.Button(
    frame_bottoni,
    text="Nuovo",
    image=icone["nuovo"],
    compound="left",
    command=editor_persona
)
btn_nuovo.pack(side="left", padx=5)

btn_modifica = tk.Button(
    frame_bottoni,
    text="Modifica",
    image=icone["modifica"],
    compound="left",
    command=modifica_persona
)
btn_modifica.pack(side="left", padx=5)

btn_elimina = tk.Button(
    frame_bottoni,
    text="Elimina",
    image=icone["elimina"],
    compound="left",
    command=elimina_persona
)
btn_elimina.pack(side="left", padx=5)


# Caricamento iniziale e avvio
carica_persone()
aggiorna_tabella()
mostra_login()
finestra.mainloop()
