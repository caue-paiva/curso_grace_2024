#ambiente de teste
'''Esse programa faz a leitura de uma lista de alunos registrada num arquivo (notas.in).
O programa calcula a média das notas de cada aluno e verifica se o aluno foi ou não 
aprovado na disciplina. Os resultados são impressos num novo arquivo “resultado.txt”.'''

#########
#Função para calcular média entre N números. 
#Recebe como parêmetro de entrada a lista de notas de um aluno.
def mediaN (valores):
  quantidade = len ( valores ) #Calcula a quantidade de notas do aluno na lista.
  soma = 0 #inicializa a variável soma com valor de zero.
  for i in range ( quantidade ): #laço FOR que percorre a lista de notas do aluno.
    soma = soma + valores [ i ] # acumula a soma das notas do aluno.
  resultado = soma / quantidade #calcula a média das notas do aluno.
  return resultado #retorna o valor da média das notas do aluno.


#########
#Função que realiza a leitura do arquivo de entrada.
def ler_entrada(nome_do_arquivo):
    with open(nome_do_arquivo) as notas: #abre o arquivo de entrada e o renomeia como sendo a variável notas.
        dados = notas.readlines() #lê todas as linhas do arquivo e as armazena na variável dados.
        #Laço FOR que percorre cada linha da variável dados
        for i in range(len(dados)): 
            dados[i] = dados[i].rstrip("\n").split() #A função 'rstrip' remove o caractere de quebra de linha '\n'. A função 'split' separa cada linha e a converte numa sub-lista que será armazenada em dados[i]. 
            #Laço FOR que percorre cada sub-lista da variável dados.
            for j in range(1, len(dados[i])): 
                dados[i][j] = int(dados[i][j]) #converte os valores de cada valor [j] na sublista dados[i] para inteiro.

        return dados #retorna a lista de 'dados' com i linhas e j colunas.

#########
#Função que verifica os alunos aprovados
def verifica_aprovados(notas):
    numero_alunos = len(notas) #calcula a quantidade de linhas da lista 'notas'
    for i in range(numero_alunos):
        nome = notas[0] #recupera o nome do aluno que está na coluna [0] e na linha [i] da lista 'notas'
        media = mediaN(notas[i][1:]) #chama a função 'mediaN' para calcular a média das notas do aluno que estão a partir da coluna [1] da lista 'notas'
        media = round(media, 1) #arredonda a média para uma casa decimal
        notas[i].append(media) #adiciona a média do aluno na última coluna da lista 'notas'
        if media >= 7.0: #verifica se a média do aluno é maior ou igual a sete
            notas[i].append("Aprovado") #adiciona a palavra 'Aprovado' na última coluna da lista 'notas'
        else: #caso contrário:
            notas[i].append("Reprovado") #adiciona a palavra 'Reprovado' na última coluna da lista 'notas'
    return notas #retorna a lista 'notas' com as informações atualizadas.

#########
#Função que escreve no arquivo de saída.
def exporta_resultado(notas): #recebe como parâmetro de entrada a lista 'notas'
    arquivo = open("resultado.txt", "w") #abre o arquivo de saída e o renomeia como sendo a variável arquivo.
    numero_alunos = len(notas) #calcula a quantidade de linhas da lista 'notas', sendo que cada linha corresponde a um aluno.
    for i in range(numero_alunos): #laço FOR que percorre cada linha da lista 'notas'
        nome = notas[i][0] #recupera o nome do aluno que está na coluna [0] e na linha [i] da lista
        situacao = notas[i][-1] #recupera a situação do aluno que está na última coluna [-1] e na linha [i] da lista notas
        arquivo.write("O aluno " + nome + " foi " + situacao + "\n") #escreve no arquivo de saída a mensagem com o nome do aluno e sua situação
    arquivo.close() #fecha o arquivo de saída

def exporta_resultado_2(notas):
    with open("resultado.txt", "w") as resultado2: #abre o arquivo de entrada e o renomeia como sendo a variável resultado_2.
        numero_alunos = len(notas) #calcula a quantidade de linhas da lista notas
        aprovados = 0 
        reprovados = 0 

        for i in range(numero_alunos):
            situacao = notas[i][-1] #A função verifica_aprovados(notas) calcula a média e adiciona "Aprovado" ou "Reprovado" à lista notas, assim é possivel a recuperação da situação do aluno. 
            if situacao == "Aprovado":
                aprovados += 1
            else:
                reprovados += 1

    return [aprovados, reprovados] #retorna uma lista com a quantidade de alunos aprovados e reprovados.

##########################
#O programa começa aqui
notas = ler_entrada("notas.in") #Chama a função que lê o arquivo de entrada e armazena o valor retornado na variável 'notas'
notas = verifica_aprovados(notas) #Chama a função que realiza a verificação e armazena o valor retornado na variável 'notas'
aprovados = exporta_resultado_2(notas) #Chama a função que escreve o arquivo de saida e armazena o valor na varivel 'aprovados'
exporta_resultado(notas) # Chama a função que exporta o resultado em um arquivo

#Laço FOR que percorre cada linha da variável 'notas'
for i in range(len(notas)): 
  print(notas[i]) #imprime os valores de cada linha da variável 'notas'

print("\nO número de aprovados é: ", aprovados[0])
print("O número de reprovados é: ", aprovados[1])


