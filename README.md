# 🛠 Instalador de Programas – Pós-formatação (Uso Interno)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![Sistema](https://img.shields.io/badge/Sistema-Windows-blue)
![Uso-Interno](https://img.shields.io/badge/Uso-Interno-informational)

Este é um instalador personalizado e simplificado, criado para facilitar a reinstalação de programas essenciais após a formatação de computadores em ambientes internos.  
Pensado especialmente para **técnicos do setor de informática**.

Desenvolvido com **Python** e **CustomTkinter**, o instalador oferece uma interface gráfica intuitiva e objetiva, permitindo ao usuário selecionar com checkboxes quais programas deseja instalar.  
Os arquivos de instalação ficam salvos localmente na pasta `programas/`, e cada instalação é executada em **modo silencioso** sempre que possível.

## 🚨 Observação/ALERTA

Algumas versões do Windows irão indicar como **NÃO SEGURO**, porém é devido ao modelo de formatação do python e do customTkInter, caso queira checar manualmente se não estiver confiante, pode utilizar o VirustTotal.com para verificar se há virus ou não.
[VirusTotal](https://www.virustotal.com/gui/home/upload)

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

1. Baixe como arquivo ZIP ou clone o repositório em uma pasta desejada.
2. Inicie o programa em "InstaladorDeProgramas/dist/InstallProV.01.exe"- O windows provavelmente vai indicar como NÃO SEGURO, porém é devido ao modelo de formatação do python e do customTkInter, caso queira checar manualmente se não estiver confiante, pode utilizar o VirustTotal.com para verificar se há virus ou não.
3. Inicie o script `instaladorProgramas.py` caso queria modificar ou o atalho `InstallProV01.exe` para iniciar o programa  
4. Marque os programas que deseja instalar( É possível adicionar seu programa, bem como exclui-lo também )
5. Clique em **“Instalar”** e aguarde a conclusão
6. SEMPRE DÊ OK NAS CAIXAS PARA PROSSEGUIR COM A INSTALAÇÃO CASO CONTRÁRIO ELA NÃO IRÁ INICIAR 

---

## 💡 Observação

Este projeto é voltado para **uso interno** por equipes de TI, técnicos ou profissionais que fazem reinstalações frequentes e desejam automatizar o processo básico de setup pós-formatação.

---

## 💡 Futuras implementações

Adicão de automação Python para instalação de programas. Utilização de Bash para instalações mais fluidas. Interface melhorada.

---

📌 *Sinta-se à vontade para adaptar este projeto ao seu fluxo interno. Sugestões são sempre bem-vindas!*
