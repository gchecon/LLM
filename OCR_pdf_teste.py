from tika import parser
import os

def extrair_texto_pdf(caminho_pdf):
  """
  Extrai texto de um PDF com imagens usando Apache Tika.

  Args:
    caminho_pdf: Caminho para o arquivo PDF.

  Returns:
    Texto extraído do PDF.
  """


def extrair_texto_pdf_com_imagens(caminho_arquivo):
    # Inicializa o parser do Tika
    parsed = parser.from_file(caminho_arquivo, serverEndpoint='http://localhost:9998/')

    # Extrai o texto
    texto_extraido = parsed["content"]

    # Certifique-se de que texto_extraido não é None ou outra verificação, conforme necessário
    if texto_extraido:
        # Limpa espaços em branco extras
        texto_limpo = "\n".join([linha.strip() for linha in texto_extraido.splitlines() if linha.strip()])
    else:
        texto_limpo = ""

    return texto_limpo


def obter_arquivo():
  while True:
    caminho_pdf = input("Digite o nome do arquivo PDF: ")
    if not os.path.exists(caminho_pdf):
      print("Arquivo não encontrado.")
      continue

    if not caminho_pdf.endswith('.pdf'):
      print("O arquivo precisa ser um PDF.")
      continue

    return caminho_pdf


path_pdf = obter_arquivo()
texto_extraido = extrair_texto_pdf_com_imagens(path_pdf)

nome_arquivo, extensao = os.path.splitext(os.path.basename(path_pdf))
nome_arquivo_txt = f"{nome_arquivo}.txt"
path_arquivo_txt = os.path.join(os.path.dirname(path_pdf), nome_arquivo_txt)

try:
  with open(path_arquivo_txt, "w") as arquivo:
    arquivo.write(texto_extraido)
except Exception as e:
  print(f"Erro ao salvar texto no arquivo TXT: {e}")
