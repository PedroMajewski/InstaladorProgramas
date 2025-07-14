#Dependências
from textwrap import fill
import customtkinter as ctk
import subprocess
import os
from tkinter import messagebox
import time
from PIL import Image
import customtkinter
from customtkinter.windows import ctk_input_dialog
import requests
import tempfile
import threading
import shutil
from customtkinter import CTkInputDialog
from DatabaseSQL import DatabaseManager

#Mudar a cor do Programa
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

#Faz a Comunicação com o database
db = DatabaseManager()
programas_cadastrados = db.buscar_programa()

# Dicionário para armazenar os checkboxes
checkboxes = {}
isCheckBoxMarcado = True
EscritaBtn = "Desmarcar todos os progarmas"

# Função para desmarcar todos os checkboxes
def desmarcar_todos():
    global isCheckBoxMarcado, EscritaBtn
    if isCheckBoxMarcado is False:
        for var in checkboxes.values():
            var.set(True)
            isCheckBoxMarcado = True
            EscritaBtn = "Desmarcar todos os programas"
    else:
        for var in checkboxes.values():
            var.set(False)
            isCheckBoxMarcado = False
            EscritaBtn = "Marcar todos os programas"

#Função que verifica se o arquivo é local ou é um URL da Web
def verificar_arquivo_local(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        return caminho_arquivo
    return None

#Função de baixar o instalador direto via link
def baixar_instalador(url, nome_programa):
    try:
        # Verifica se é um arquivo local
        if not url.startswith(('http://', 'https://')):
            caminho_local = verificar_arquivo_local(url)
            if caminho_local:
                # Copia o arquivo para a pasta temporária
                temp_dir = os.path.join(tempfile.gettempdir(), "InstallPro")
                os.makedirs(temp_dir, exist_ok=True)
                temp_file = os.path.join(temp_dir, os.path.basename(url))
                shutil.copy2(caminho_local, temp_file)
                return temp_file
            else:
                messagebox.showerror("Erro", f"Arquivo local não encontrado: {url}")
                return None
        
        # Se for URL, baixa normalmente
        temp_dir = os.path.join(tempfile.gettempdir(), "InstallPro")
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, f"{nome_programa}.exe")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        
        with open(temp_file, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
        
        return temp_file
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar {nome_programa}: {str(e)}")
        return None

#Função de Inicializar o instalador
def instalar_programas():
    programas_cadastrados = db.buscar_programa()
    # Crie um dicionário para mapear nome -> caminhoArquivo
    caminhos = {prog[1]: prog[2] for prog in programas_cadastrados}
    programas_selecionados = [nome for nome, var in checkboxes.items() if var.get()]
    if not programas_selecionados:
        messagebox.showwarning("Aviso", "Selecione pelo menos um programa para instalar!")
        return

    for nome in programas_selecionados:
        url = caminhos[nome]
        
        # Verifica se é um arquivo local
        if not url.startswith(('http://', 'https://')):
            messagebox.showinfo("Instalação", f"Preparando instalação do {nome}")
        else:
            messagebox.showinfo("Download", f"Iniciando download do {nome}")
        
        def download_e_instalar():
            temp_file = baixar_instalador(url, nome)
            if temp_file:
                try:
                    subprocess.Popen([temp_file], shell=True)
                    messagebox.showinfo("Instalação", f"Iniciando instalação do {nome}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao instalar {nome}: {str(e)}")
        
        threading.Thread(target=download_e_instalar).start()

#Função de instalar todos os programas
def instalar_todos_automaticamente():
    programas_cadastrados = db.buscar_programa()
    caminhos = {prog[1]: prog[2] for prog in programas_cadastrados}
    nomes_programas = [prog[1] for prog in programas_cadastrados]

    if not nomes_programas:
        messagebox.showwarning("Aviso", "Nenhum programa cadastrado para instalar!")
        return

    if not messagebox.askyesno("Confirmação", "Deseja instalar todos os programas automaticamente?"):
        return

    def instalar_programa(nome, url):
        if not url.startswith(('http://', 'https://')):
            messagebox.showinfo("Instalação", f"Preparando instalação do {nome}")
        else:
            messagebox.showinfo("Download", f"Iniciando download do {nome}")

        temp_file = baixar_instalador(url, nome)
        if temp_file:
            try:
                subprocess.Popen(f'"{temp_file}" /S', shell=True)
                time.sleep(2)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao instalar {nome}: {str(e)}")

    for nome in nomes_programas:
        url = caminhos[nome]
        threading.Thread(target=instalar_programa, args=(nome, url)).start()

    messagebox.showinfo("Concluído", "Todos os programas foram iniciados para instalação!")

#Função de Adicionar um programa ao instalador
def adicionar_programa():

    # Solicita ao usuário o nome do programa
    nome = customtkinter.CTkInputDialog(text="Digite o nome do Programa", title="Adicionar Programa:").get_input()
    if not nome:
        messagebox.showwarning("Aviso", "Nome do programa não informado.")
        return

    # Solicita ao usuário o caminho do arquivo ou link
    caminho = customtkinter.CTkInputDialog(title= "Adicionar Programa", text = "Digite o caminho do arquivo ou link do programa:").get_input()
    if not caminho:
        messagebox.showwarning("Aviso", "Caminho do arquivo não informado.")
        return

    db = DatabaseManager()
    sucesso = db.adicionar_programa(nome, caminho)
    if sucesso:
        messagebox.showinfo("Sucesso", f"Programa '{nome}' adicionado com sucesso ao banco de dados!")
        renderizarProgramas()
    else:
        messagebox.showerror("Erro", "Não foi possível adicionar o programa ao banco de dados.")

#Função de Remover um programa ao instalador
def remover_programa(programa):
    janelaAlerta = messagebox.askyesno(title="Excluir Programa", message="Deseja mesmo excluir o programa?")
    if janelaAlerta:
        db.remover_programa(programa)
        renderizarProgramas()
    else:
        messagebox.showerror("Erro", "Programa não removido.")

#Função de Renderizar a lista dos programas
def renderizarProgramas():
    # Limpa todos os widgets do frame antes de renderizar novamente
    for widget in frame_programas.winfo_children():
        widget.destroy()
    checkboxes.clear()

    # Atualiza a lista de programas do banco
    programas_cadastrados = db.buscar_programa()

    # SubTítulo
    subtitulo = ctk.CTkLabel(frame_programas, text="Selecione os programas para instalar:", font=("Arial", 14, "normal"))
    subtitulo.pack(pady=10)

    trash_icon = ctk.CTkImage(
                light_image=Image.open(trash_img),
                dark_image=Image.open(trash_img),
                size=(24, 24)
            )

    for prog in programas_cadastrados:
        nome = prog[1]
        caminhopath = prog[2]
        max_length = 80
        if len(caminhopath) > max_length:
            texto_caminho = caminhopath[:max_length-3] + "..."
        else:
            texto_caminho = caminhopath
        var = ctk.BooleanVar(value=True)

        # Frame principal da linha
        frame_linha = ctk.CTkFrame(frame_programas)
        frame_linha.pack(fill="x", padx=5, pady=2)

        # Frame da esquerda (checkbox + descrição)
        frame_esquerda = ctk.CTkFrame(frame_linha, fg_color="transparent")
        frame_esquerda.pack(side="left", fill="both", expand=True)

        checkbox = ctk.CTkCheckBox(
            frame_esquerda, 
            text=nome, 
            variable=var, 
            corner_radius=0, 
            font=("Arial", 14, "bold")
        )
        checkbox.pack(pady=(5, 0), padx=10, anchor="w")
        checkboxes[nome] = var

        description = ctk.CTkLabel(
            frame_esquerda, 
            text=texto_caminho, 
            font=("Arial", 12, "normal"),
            anchor="w"
        )
        description.pack(pady=(0, 10), padx=20, anchor="w")

        # Frame da direita (botões)
        frame_direita = ctk.CTkFrame(frame_linha, fg_color="transparent")
        frame_direita.pack(side="right", padx=10, pady=5)

        btnRemoverPrograma = ctk.CTkButton(
            frame_direita,
            image=trash_icon,
            text="",
            command=lambda pid=prog[0]: remover_programa(pid),
            width=25,
            height=25,
            fg_color="#aa2913",
            hover_color="#7c291b",
            corner_radius=4
        )
        btnRemoverPrograma.pack(side="right", padx=(5, 0))

        # Botão de copiar caminho
        def copiar_caminho(caminho=caminhopath):
            janelaInstalador.clipboard_clear()
            janelaInstalador.clipboard_append(caminho)
            messagebox.showinfo("Caminho copiado", "O caminho foi copiado para a área de transferência.")

        btnCopiarCaminho = ctk.CTkButton(
            frame_direita,
            text="Copiar Caminho",
            command=lambda caminho=caminhopath: copiar_caminho(caminho),
            width=120,
            height=35,
            corner_radius=4
        )
        btnCopiarCaminho.pack(side="right", padx=(0, 5))

    # Se não houver programas cadastrados, exibe uma mensagem
    if not programas_cadastrados:
        frameSemPrograma = ctk.CTkLabel(frame_programas, text="Sem programas adicionados até o momento :(", font=("Arial", 16, "bold"))
        frameSemPrograma.pack(pady=20)

#Caminhos renderizados para o .exe
caminho_ico = os.path.join(os.path.dirname(__file__), "assets", "InstallPro.ico")
caminho_logo_img = os.path.join(os.path.dirname(__file__), "assets", "InstallPro.png")
trash_img = os.path.join(os.path.dirname(__file__), "assets", "trash.png")
linkedin_img = os.path.join(os.path.dirname(__file__), "assets", "linkedin.png")

# Configuração da janela principal
janelaInstalador = ctk.CTk()
janelaInstalador.title("InstallPro")
janelaInstalador.iconbitmap(caminho_ico)
janelaInstalador.geometry("800x600")
janelaInstalador.resizable(False, False)

# Carregar e exibir a logo
try:
    # Carregar a imagem usando CTkImage
    logo_img = ctk.CTkImage(
        light_image=Image.open(caminho_logo_img),
        dark_image=Image.open(caminho_logo_img),
        size=(60, 60)
    )
    
    # Criar label para a logo
    logo_label = ctk.CTkLabel(janelaInstalador, image=logo_img, text="")
    logo_label.pack(pady=2)
except Exception as e:
    print(f"Erro ao carregar a logo: {e}")

#Titulo
titulo = ctk.CTkLabel(janelaInstalador, text="Instalador de Programas InstallPro", font=("Helvetica", 18, "normal"))
titulo.pack(pady=10)

def abrir_linkedin(event=None):
    import webbrowser
    webbrowser.open_new("https://br.linkedin.com/in/pedro-henrique-majewski-de-souza-e-silva")

marca = ctk.CTkLabel(
    janelaInstalador, 
    text="Criado por Pedro Henrique Majewski (LinkedIn)", 
    font=("Helvetica", 14, "normal"), 
    text_color="#E69202",  # cor azul do LinkedIn
    cursor="hand2"
)
marca.pack(pady=4)
marca.bind("<Button-1>", abrir_linkedin)

# Botão de desmarcar todos
botao_desmarcar = ctk.CTkButton(
    janelaInstalador,
    text="Desmarcar/Marcar programas",
    command=desmarcar_todos,
    width=180,
    height=20,
    fg_color="#757575",
    hover_color="#636363",
    corner_radius=0
)
botao_desmarcar.pack(fill="both",padx=20, expand=True)

# Frame para os checkboxes
frame_programas = ctk.CTkScrollableFrame(janelaInstalador, width=600, height=300, corner_radius=0)
frame_programas.pack(pady=20, padx=20, fill="both", expand=True)

renderizarProgramas()

# Frame para os botões
frame_botoes = ctk.CTkFrame(janelaInstalador, bg_color="transparent")
frame_botoes.pack(pady=20)

# Botão de instalação manual
botao_instalar = ctk.CTkButton(
    frame_botoes,
    text="Instalar Programas Selecionados",
    command=instalar_programas,
    width=300,
    height=40,
    corner_radius=0
)
botao_instalar.pack(side="left", padx=10)

# Botão de instalação automática
botao_auto = ctk.CTkButton(
    frame_botoes,
    text="Instalar todos os programas",
    command=instalar_todos_automaticamente,
    width=300,
    height=40,
    fg_color="#E69202",
    hover_color="#C77F02",
    corner_radius=0
)
botao_auto.pack(side="left", padx=10)

botao_add = ctk.CTkButton(
    frame_botoes,
    text="+ Adicionar Programa",
    command=adicionar_programa,
    width=300,
    height=40,
    fg_color="#2E7D32",  # Verde
    hover_color="#1B5E20",
    corner_radius=0
)
botao_add.pack(side="left", padx=10)

janelaInstalador.mainloop()
