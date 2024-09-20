import sqlite3
from tkinter import *
from tkinter import ttk

# Função para criar a conexão com o banco de dados
def conectar_banco():
    return sqlite3.connect('primeiro_banco.db')

# Função para criar a tabela, se ainda não existir
def criar_tabela():
    with conectar_banco() as banco:
        cursor = banco.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                materia TEXT,
                nome_do_aluno TEXT UNIQUE,
                prova REAL,
                teste REAL,
                media REAL,
                aprovados TEXT
            )
        """)
        banco.commit()

# Função para calcular a média e definir aprovação
def calcular_media(prova, teste):
    media = round((prova + teste) / 2, 2)
    aprovado = 'sim' if media >= 6 else 'não'
    return media, aprovado

# Função para inserir os dados de um aluno
def inserir_dados():
    nome = entry_nome.get()
    prova = float(entry_prova.get())
    teste = float(entry_teste.get())
    materia = materia_selecionada.get()  
    media, aprovado = calcular_media(prova, teste)

    with conectar_banco() as banco:
        cursor = banco.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO alunos (materia, nome_do_aluno, prova, teste, media, aprovados)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (materia, nome, prova, teste, media, aprovado))

        banco.commit()

    limpar_campos()

# Função para excluir os dados de um aluno
def excluir_dados():
    nome = entry_nome.get()
    materia = materia_selecionada.get()  
    
    with conectar_banco() as banco:
        cursor = banco.cursor()
        cursor.execute("DELETE FROM alunos WHERE nome_do_aluno = ? AND materia = ?", (nome, materia))
        banco.commit()

    label_mensagem.config(text=f"Aluno {nome} excluído com sucesso.")

    limpar_campos()

# Função para visualizar os dados em uma nova janela
def visualizar_dados():
    materia = materia_selecionada.get() 

    nova_janela = Toplevel()
    nova_janela.title(f"Visualizar Dados da turma {materia}")

    largura_tela = nova_janela.winfo_screenwidth()
    altura_tela = nova_janela.winfo_screenheight()

    # Definir a geometria da nova janela
    largura_nova_janela = int(largura_tela * 0.65)
    altura_nova_janela = int(altura_tela * 0.7)
    nova_janela.geometry(f"{largura_nova_janela}x{altura_nova_janela}+630+90")

    # Conectando ao banco de dados para buscar os dados
    with conectar_banco() as banco:
        cursor = banco.cursor()
        cursor.execute("""
            SELECT materia, nome_do_aluno, prova, teste, media, aprovados
            FROM alunos
            WHERE materia = ?
            ORDER BY nome_do_aluno
        """, (materia,))
        alunos = cursor.fetchall()

    # Criando uma tabela para exibir os dados
    tabela = ttk.Treeview(nova_janela, columns=("Materia", "Nome", "Prova", "Teste", "Média", "Aprovado"), show="headings", height=35)
    tabela.heading("Materia", text="Matéria")
    tabela.heading("Nome", text="Nome do Aluno")
    tabela.heading("Prova", text="Prova")
    tabela.heading("Teste", text="Teste")
    tabela.heading("Média", text="Média")
    tabela.heading("Aprovado", text="Aprovado")

    tabela.grid(row=0, column=0, padx=20, pady=20)
    
    # Inserindo os dados na tabela
    for aluno in alunos:
        tabela.insert("", "end", values=aluno)
    
# Função para limpar os campos de entrada
def limpar_campos():
    entry_nome.delete(0, END)
    entry_prova.delete(0, END)
    entry_teste.delete(0, END)

def next_entry(event, next_widget):
    next_widget.focus_set()

# Função principal para criação da interface
def criar_interface():
    janela = Tk()
    janela.title("Planilha dos Alunos")

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Definir a geometria da janela principal
    largura_janela = int(largura_tela * 0.5)
    altura_janela = int(altura_tela * 0.7)
    janela.geometry(f"{largura_janela}x{altura_janela}+20+90")

    # Configurando a distribuição das colunas para que o conteúdo seja centralizado
    janela.grid_columnconfigure(0, weight=1)
    janela.grid_columnconfigure(1, weight=1)
    
    # Configurando também as linhas para distribuir melhor os elementos
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_rowconfigure(10, weight=1)  # Última linha
    
    # Cabeçalho centralizado
    Label(janela, text="Centro Educacional Positivo", font=("Cambria", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew")
    Label(janela, text="Lot. Sol Nascente QC, Rua: MªIsabel de Lima,101 Aut.Port.nº001/06/12 de 09/01/2006", font=("Cambria", 16)).grid(row=1, column=0, columnspan=2, sticky="nsew")
    Label(janela, text="CNPJ 07.184.049/0001-90           Fone: 75 99118-1256 / 98124-2241", font=("Cambria", 16)).grid(row=2, column=0, columnspan=2, sticky="nsew")
    Label(janela, text="Email: positivoaulasremotas@gmail.com", font=("Calibri", 14)).grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
    
    # Lista de matérias para o OptionMenu
    materias = ["Inglês", "Português", "História", "Ciências", "Matemática", "Geografia", "Ética", "Ed.Física"]
    global materia_selecionada
    materia_selecionada = StringVar(janela)
    materia_selecionada.set(materias[0])
    
    # Campo de entrada
    Label(janela, text="Nome da matéria", font=("System", 18)).grid(row=4, column=0, sticky="e")
    option_menu_materia = OptionMenu(janela, materia_selecionada, *materias)
    option_menu_materia.config(font=("Arial", 18))
    option_menu_materia.grid(row=4, column=1, sticky="w")
    
    Label(janela, text="Nome do aluno", font=("System", 18)).grid(row=5, column=0, sticky="e")
    global entry_nome
    entry_nome = Entry(janela, font=("Arial", 16))
    entry_nome.grid(row=5, column=1, sticky="w")
    entry_nome.bind("<Return>", lambda event: next_entry(event, entry_prova))
    
    Label(janela, text="Nota da prova", font=("System", 18)).grid(row=6, column=0, sticky="e")
    global entry_prova
    entry_prova = Entry(janela, font=("Arial", 16))
    entry_prova.grid(row=6, column=1, sticky="w")
    entry_prova.bind("<Return>", lambda event: next_entry(event, entry_teste))
    
    Label(janela, text="Nota do teste", font=("System", 18)).grid(row=7, column=0, sticky="e")
    global entry_teste
    entry_teste = Entry(janela, font=("Arial", 16))
    entry_teste.grid(row=7, column=1, sticky="w")
    entry_teste.bind("<Return>", lambda event: inserir_dados())
    
    # Botões centralizados
    Button(janela, text="Adicione um novo aluno", font=("Arial", 15), command=inserir_dados).grid(row=8, column=0, sticky="e", pady=10)
    Button(janela, text="Exclua um dado de um aluno", font=("Arial", 15), command=excluir_dados).grid(row=8, column=1, sticky="w", pady=10)
    Button(janela, text="Aperte para visualizar os dados desta matéria", font=("Arial", 15), command=visualizar_dados).grid(row=9, column=0, columnspan=2, pady=10)


    # Para mostrar mensagens
    global label_mensagem
    label_mensagem = Label(janela, text="")
    label_mensagem.grid(row=11, column=0, columnspan=2)

    janela.mainloop()

# Inicializa a aplicação criando a tabela e interface
if __name__ == "__main__":
    criar_tabela()
    criar_interface()