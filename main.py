import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

selected_folder = ""
moved_folder_path = ""
app_name = ""
executable_path = ""
icon_path = ""


def move_folder_sudo(origem, destino):
    try:
        origem = os.path.expanduser(origem)
        comando = ["sudo", "mv", origem, destino]
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        print(f"Pasta movida de {origem} para {destino} com sucesso.")
        print(f"Saída do comando:\n{resultado.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao mover pasta: {e}")
        print(f"Stderr:\n{e.stderr}")
        return False


def selecionar_pasta():
    global selected_folder
    pasta_selecionada = filedialog.askdirectory(title="Selecione a Pasta")
    if pasta_selecionada:
        selected_folder = pasta_selecionada
        caminho_pasta.config(text=pasta_selecionada)
        print(f"Pasta selecionada: {pasta_selecionada}")



def mover_pasta():
    global moved_folder_path, app_name
    app_name = app_name_entry.get()  # Get the app name directly
    if selected_folder and app_name:
        destino = "/opt/"
        moved_folder_name = app_name
        moved_folder_path = os.path.join(destino, moved_folder_name)
        if move_folder_sudo(selected_folder, moved_folder_path):
           print(f"Moved folder to: {moved_folder_path}")
        else:
            print("Error moving folder.")
    else:
        print("Selecione uma pasta e insira o nome do aplicativo!")
        messagebox.showerror("Erro", "Selecione uma pasta e insira o nome do aplicativo!")


def selecionar_arquivo():
    global executable_path
    if moved_folder_path:
        executable_path = filedialog.askopenfilename(
            title="Selecione o executável",
            initialdir=moved_folder_path
        )
        if executable_path:
            caminho_arquivo.config(text=executable_path)
            print(f"Arquivo selecionado: {executable_path}")
    else:
        print("Mova a pasta primeiro!")

def selecionar_icone():
    global icon_path
    if moved_folder_path:
      icon_path = filedialog.askopenfilename(
          title="Selecione o ícone",
          initialdir=moved_folder_path
      )
    if icon_path:
      print(f"Ícone selecionado: {icon_path}")

def criar_desktop_file():
    global app_name, moved_folder_path, executable_path, icon_path
    app_name = app_name_entry.get()
    if app_name and moved_folder_path and executable_path:
        desktop_file_name = f"{app_name}.desktop"
        desktop_file_path = os.path.join("/usr/share/applications", desktop_file_name)
        desktop_content = f"""
        [Desktop Entry]
        Version=1.0
        Type=Application
        Name={app_name}
        Exec={executable_path}
        Icon={icon_path if icon_path else ""}
        Terminal=false
        Categories=Utility;
        """
        try:
            with subprocess.Popen(["sudo", "tee", desktop_file_path], stdin=subprocess.PIPE, text=True) as process:
              process.communicate(desktop_content)
            subprocess.run(["sudo", "chmod", "+x", desktop_file_path], check=True)

            print(f"Arquivo .desktop criado em: {desktop_file_path}")
            messagebox.showinfo("Sucesso", f"Arquivo .desktop criado em:\n{desktop_file_path}")
        except Exception as e:
            print(f"Erro ao criar arquivo .desktop: {e}")
            messagebox.showerror("Erro", f"Erro ao criar arquivo .desktop:\n{e}")
    else:
        print("Selecione uma pasta, insira o nome do aplicativo, mova a pasta e selecione um executável!")
        messagebox.showerror("Erro", "Selecione uma pasta, insira o nome do aplicativo, mova a pasta e selecione um executável!")

janela = tk.Tk()
janela.title("Selecionar Pasta")

label_instrucao = tk.Label(janela, text="Selecione a pasta que deseja mover:")
label_instrucao.pack(pady=10)

botao_selecionar = tk.Button(janela, text="Selecionar Pasta", command=selecionar_pasta)
botao_selecionar.pack(pady=10)

caminho_pasta = tk.Label(janela, text="")
caminho_pasta.pack(pady=5)

# Input for the app name
app_name_label = tk.Label(janela, text="Nome do Aplicativo:")
app_name_label.pack(pady=5)

app_name_entry = tk.Entry(janela)
app_name_entry.pack(pady=5)


botao_mover = tk.Button(janela, text="Mover", command=mover_pasta)
botao_mover.pack(pady=10)

botao_selecionar_arquivo = tk.Button(janela, text="Selecionar Executável", command=selecionar_arquivo)
botao_selecionar_arquivo.pack(pady=10)

caminho_arquivo = tk.Label(janela, text="")
caminho_arquivo.pack(pady=5)


botao_selecionar_icone = tk.Button(janela, text = "Selecionar Ícone", command=selecionar_icone)
botao_selecionar_icone.pack(pady=10)

botao_criar_desktop = tk.Button(janela, text="Criar Atalho", command=criar_desktop_file)
botao_criar_desktop.pack(pady=10)

janela.mainloop()
