# 🛠 Instalador de Programas – Pós-formatação (Uso Interno)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![Sistema](https://img.shields.io/badge/Sistema-Windows-blue)
![Uso-Interno](https://img.shields.io/badge/Uso-Interno-informational)

Este é um instalador personalizado e simplificado, criado para facilitar a reinstalação de programas essenciais após a formatação de computadores em ambientes internos.  
Pensado especialmente para **técnicos do setor de informática**.

Desenvolvido com **Python** e **CustomTkinter**, o instalador oferece uma interface gráfica intuitiva e objetiva, permitindo ao usuário selecionar com checkboxes quais programas deseja instalar.  
Os arquivos de instalação ficam salvos localmente na pasta `programas/`, e cada instalação é executada em **modo silencioso** sempre que possível.

---

## 🔧 Funcionalidades

- ✅ Interface gráfica simples e direta  
- ✅ Checkboxes para seleção de programas  
- ✅ Execução de instaladores com parâmetros silenciosos  
- ✅ Mensagens de sucesso ou erro para cada instalação  
- ✅ Uso totalmente offline (sem necessidade de internet)  
- ✅ Projeto leve, ideal para uso interno ou técnico  

---

## 📁 Estrutura do Projeto

InstaladorGeral/
├── instalar.py # Script principal com a lógica e a interface
├── iniciar.bat # (Opcional) Atalho para executar o script
├── programas/ # Instaladores locais (.exe)
│ ├── ChromeSetup.exe
│ ├── FirefoxSetup.exe
│ └── ...
├── SolidDataBase.db # (Opcional) Base de dados auxiliar se desejado

## 🚀 Como usar

1. Coloque os instaladores desejados na pasta `programas/`  
   *(ou insira o link de download do seu programa, se implementar essa funcionalidade)*  
2. Inicie o script `instalar.py` ou o atalho `Instalador de Programas.exe` (caso compilado com PyInstaller)  
3. Marque os programas que deseja instalar  
4. Clique em **“Instalar”** e aguarde a conclusão  

---

## ✅ Requisitos

- Sistema **Windows**
- **Python 3.x**
- Bibliotecas necessárias:
  - `customtkinter` → instale com:
    ```bash
    pip install customtkinter
    ```

---

## 💡 Observação

Este projeto é voltado para **uso interno** por equipes de TI, técnicos ou profissionais que fazem reinstalações frequentes e desejam automatizar o processo básico de setup pós-formatação.

---

📌 *Sinta-se à vontade para adaptar este projeto ao seu fluxo interno. Sugestões são bem-vindas!*
