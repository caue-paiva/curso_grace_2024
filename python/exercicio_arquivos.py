import os


#Função para calcular média entre N números
def mediaN (valores:list[int])->float:
	return sum(valores)/len(valores)

def ler_entrada(nome_do_arquivo:str)->str:
   PATH: str = os.path.join(os.getcwd(), nome_do_arquivo)
   dados_lidos:str
   with open(PATH,"r") as f:
      dados_lidos =  f.read()
   return dados_lidos

def lista_strings_para_numeros(lista:list[str])->list[int]:
   nova_lista = []
   for num in lista:
       nova_lista.append(int(num))
   
   return nova_lista
        
def separa_entrada(conteudos_arquivo:str)->list[dict]:
   linhas:list[str] = conteudos_arquivo.split("\n")
   lista_alunos:list[dict] = []
   for linha in linhas:
       lista_campos:list[str] = linha.split(" ")
       notas:list[int] = lista_strings_para_numeros(lista_campos[1:])
       lista_alunos.append(
           {
               "nome":lista_campos[0],
               "notas":notas
           }
       )
   return lista_alunos

#Função que verifica os alunos aprovados
def verifica_aprovados(notas:str)->str:
   lista_alunos:list[dict] = separa_entrada(notas)

   RESULTADO_ALUNO_TEMPLATE = "O aluno {aluno} foi {resultado}\n"
   string_resultado:str = ""
   MEDIA_APROVACAO = 5
   for aluno in lista_alunos:
      print(aluno)
      media:float = mediaN(aluno["notas"])
      resultado:str
      if media < MEDIA_APROVACAO:
         resultado = "Reprovado"
      else:
         resultado = "Aprovado"
      string_resultado += RESULTADO_ALUNO_TEMPLATE.format(aluno= aluno["nome"], resultado = resultado)
   return string_resultado

def exporta_resultado(notas:str)->None:
   PATH: str = os.path.join(os.getcwd(),"resultado.txt")
   with open(PATH,"w") as f:
       f.write(notas)

#O programa começa aqui
notas = ler_entrada("notas.in") #Lê a entrada
notas = verifica_aprovados(notas) #Realiza a verificação
exporta_resultado(notas) #Exporta o resultado em um arquivo
