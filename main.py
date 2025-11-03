import customtkinter as ctk
from tkinter import messagebox, simpledialog
from pymongo import MongoClient
from bson import ObjectId
from cryptography.fernet import Fernet
import json, base64
from hashlib import sha256

def generate_key_from_password(password: str) -> bytes:
    digest = sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_text(text: str, password: str) -> str:
    key = generate_key_from_password(password)
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt_text(token: str, password: str) -> str:
    key = generate_key_from_password(password)
    f = Fernet(key)
    try:
        return f.decrypt(token.encode()).decode()
    except:
        raise ValueError("Senha incorreta.")

class GrimoireApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Grimório Arcano")
        self.geometry("800x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.client = None
        self.db = None
        self.collection = None

        self.connection_frame = ctk.CTkFrame(self)
        self.connection_frame.pack(pady=10)
        self.url_entry = ctk.CTkEntry(self.connection_frame, width=400, placeholder_text="URL do MongoDB Atlas")
        self.url_entry.grid(row=0, column=0, padx=10)
        self.connect_btn = ctk.CTkButton(self.connection_frame, text="Conectar", command=self.connect_db)
        self.connect_btn.grid(row=0, column=1, padx=10)

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10)
        self.title_entry = ctk.CTkEntry(self.input_frame, width=200, placeholder_text="Título do Feitiço")
        self.title_entry.grid(row=0, column=0, padx=5)
        self.ing_entry = ctk.CTkEntry(self.input_frame, width=400, placeholder_text="Ingredientes (serão criptografados)")
        self.ing_entry.grid(row=0, column=1, padx=5)
        self.pwd_entry = ctk.CTkEntry(self.input_frame, width=150, placeholder_text="Senha", show="*")
        self.pwd_entry.grid(row=0, column=2, padx=5)
        self.save_btn = ctk.CTkButton(self.input_frame, text="Salvar", command=self.save_spell)
        self.save_btn.grid(row=0, column=3, padx=5)

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(pady=10, fill="both", expand=True)
        self.listbox = ctk.CTkTextbox(self.table_frame, width=300, height=200)
        self.listbox.pack(side="left", fill="y", padx=10)
        self.output_box = ctk.CTkTextbox(self.table_frame, width=450, height=200)
        self.output_box.pack(side="right", fill="both", expand=True, padx=10)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)
        self.view_btn = ctk.CTkButton(self.button_frame, text="Visualizar", command=self.view_selected)
        self.view_btn.grid(row=0, column=0, padx=10)
        self.delete_btn = ctk.CTkButton(self.button_frame, text="Excluir", command=self.delete_selected)
        self.delete_btn.grid(row=0, column=1, padx=10)

        self.refresh_list()

    def connect_db(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Erro", "Insira a URL do MongoDB Atlas.")
            return
        try:
            self.client = MongoClient(url)
            self.db = self.client["grimoire"]
            self.collection = self.db["spells"]
            self.refresh_list()
            messagebox.showinfo("Conectado", "Conexão bem-sucedida.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na conexão: {e}")

    def refresh_list(self):
        self.listbox.delete("0.0", ctk.END)
        if self.collection is None:
            return
        try:
            for doc in self.collection.find():
                self.listbox.insert(ctk.END, f"{doc.get('title', 'Sem título')}\n")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def get_selected_record(self):
        try:
            line = self.listbox.get("sel.first", "sel.last").strip()
        except:
            messagebox.showwarning("Aviso", "Selecione um feitiço da lista.")
            return None
        if not line:
            return None
        try:
            return self.collection.find_one({"title": line})
        except:
            return None

    def save_spell(self):
        if self.collection is None:
            messagebox.showerror("Erro", "Sem conexão com o MongoDB.")
            return
        title = self.title_entry.get().strip()
        ingredients = self.ing_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        if not title or not ingredients or not pwd:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        encrypted_ingredients = encrypt_text(ingredients, pwd)
        data = {"title": title, "ingredients": encrypted_ingredients}
        self.collection.insert_one(data)
        self.title_entry.delete(0, ctk.END)
        self.ing_entry.delete(0, ctk.END)
        self.pwd_entry.delete(0, ctk.END)
        self.refresh_list()
        messagebox.showinfo("Sucesso", "Feitiço salvo com sucesso.")

    def view_selected(self):
        if self.collection is None:
            messagebox.showerror("Erro", "Sem conexão com o MongoDB.")
            return
        rec = self.get_selected_record()
        if not rec:
            return
        pwd = simpledialog.askstring("Senha", "Digite a senha para descriptografar:", show="*")
        if pwd is None:
            return
        try:
            decrypted = decrypt_text(rec["ingredients"], pwd)
            self.output_box.delete("0.0", ctk.END)
            output = f"Título: {rec.get('title', 'Sem título')}\n\nIngredientes:\n{decrypted}"
            self.output_box.insert("0.0", output)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def delete_selected(self):
        if self.collection is None:
            messagebox.showerror("Erro", "Sem conexão com o MongoDB.")
            return
        rec = self.get_selected_record()
        if not rec:
            return
        pwd = simpledialog.askstring("Senha", "Digite a senha para confirmar exclusão:", show="*")
        if pwd is None:
            return
        try:
            decrypt_text(rec["ingredients"], pwd)
        except ValueError:
            messagebox.showerror("Erro", "Senha incorreta. Feitiço não excluído.")
            return
        confirm = messagebox.askyesno("Confirmar", "Deseja realmente apagar este feitiço?")
        if confirm:
            self.collection.delete_one({"_id": rec["_id"]})
            self.refresh_list()
            self.output_box.delete("0.0", ctk.END)
            messagebox.showinfo("Excluído", "Feitiço removido com sucesso.")

if __name__ == "__main__":
    app = GrimoireApp()
    app.mainloop()
