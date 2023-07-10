import tkinter as tk

# Lista de materiais
materiais = [
    {"nome": "Livro"},
    {"nome": "Caderno"},
    {"nome": "Estojo"},
    {"nome": "Lápis"},
    {"nome": "Borracha"},
    {"nome": "Régua"},
]

# Interface gráfica usando Tkinter
root = tk.Tk()
root.title("Organizador de Mochila Escolar")

# Rótulo e entrada para a capacidade da mochila
capacidade_label = tk.Label(root, text="Capacidade da mochila:")
capacidade_label.grid(row=0, column=0)

capacidade_entry = tk.Entry(root)
capacidade_entry.grid(row=0, column=1)

# Rótulo para a lista de materiais
materiais_label = tk.Label(root, text="Lista de Materiais:")
materiais_label.grid(row=1, column=0, columnspan=2)

# Quadro para conter as entradas de importância e quantidade dos materiais
materiais_frame = tk.Frame(root)
materiais_frame.grid(row=2, column=0, columnspan=2)

importancias_entries = []
quantidades_entries = []

for i, material in enumerate(materiais):
    material_label = tk.Label(materiais_frame, text=material['nome'])
    material_label.grid(row=i, column=0)

    importancia_label = tk.Label(materiais_frame, text="Importância:")
    importancia_label.grid(row=i, column=1)

    importancia_entry = tk.Entry(materiais_frame)
    importancia_entry.grid(row=i, column=2)
    importancias_entries.append(importancia_entry)

    quantidade_label = tk.Label(materiais_frame, text="Quantidade:")
    quantidade_label.grid(row=i, column=3)

    quantidade_entry = tk.Entry(materiais_frame)
    quantidade_entry.grid(row=i, column=4)
    quantidades_entries.append(quantidade_entry)

def organizar_mochila():
    capacidade_mochila = int(capacidade_entry.get())

    # Limpar lista de itens selecionados
    mochila_itens.delete(0, tk.END)

    # Atualizar a lista de itens na mochila
    pesos = []
    valores = []
    quantidade_selecionada = []
    for i, material in enumerate(materiais):
        importancia = importancias_entries[i].get()
        quantidade = quantidades_entries[i].get()
        if importancia and quantidade:
            importancia = int(importancia)
            quantidade = int(quantidade)
            if importancia <= capacidade_mochila:  # Verificar se a importância é menor ou igual à capacidade da mochila
                pesos.append(importancia)
                valores.append(quantidade)
                quantidade_selecionada.append(quantidade)

    # Ordenar os materiais em ordem decrescente de importância
    materiais_ordenados = [material for _, material in sorted(zip(pesos, materiais), reverse=True)]

    # Chamada da função do algoritmo da Mochila
    valor_total, itens_selecionados_indices = mochila(capacidade_mochila, pesos, valores, len(pesos))

    # Exibição dos itens selecionados na mochila em ordem decrescente de importância
    for indice in itens_selecionados_indices:
        item_selecionado = materiais[indice]
        importancia = importancias_entries[materiais.index(item_selecionado)].get()
        quantidade = quantidades_entries[materiais.index(item_selecionado)].get()
        mochila_itens.insert(tk.END, f"{item_selecionado['nome']} (Importância: {importancia}, Quantidade: {quantidade})")

    # Exibição do valor total na mochila
    valor_total_label.config(text=f"Valor total na mochila: {valor_total}")


# Função para organizar a mochila usando o algoritmo da Mochila
def mochila(capacidade, pesos, valores, n):
    tabela = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(capacidade + 1):
            if i == 0 or j == 0:
                tabela[i][j] = 0
            elif pesos[i - 1] <= j:
                tabela[i][j] = max(valores[i - 1] + tabela[i - 1][j - pesos[i - 1]], tabela[i - 1][j])
            else:
                tabela[i][j] = tabela[i - 1][j]

    itens_selecionados = []
    i = n
    j = capacidade
    while i > 0 and j > 0:
        if tabela[i][j] != tabela[i - 1][j]:
            itens_selecionados.append(i - 1)
            j -= pesos[i - 1]
        i -= 1

    return tabela[n][capacidade], itens_selecionados


# Botão para organizar a mochila
organizar_button = tk.Button(root, text="Organizar", command=organizar_mochila)
organizar_button.grid(row=3, column=0, columnspan=2)

# Quadro para conter os resultados
resultados_frame = tk.Frame(root)
resultados_frame.grid(row=4, column=0, columnspan=2)

# Rótulo para os itens selecionados na mochila
mochila_label = tk.Label(resultados_frame, text="Itens selecionados na mochila:")
mochila_label.grid(row=0, column=0, sticky="w")

mochila_itens = tk.Listbox(resultados_frame, width=50)
mochila_itens.grid(row=1, column=0)

# Rótulo para o valor total na mochila
valor_total_label = tk.Label(resultados_frame, text="Valor total na mochila:")
valor_total_label.grid(row=2, column=0, sticky="w")

root.mainloop()

