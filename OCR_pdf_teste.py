from tika import parser as tika_parser
import fitz
import os
import requests


def verificar_imagens_no_pdf(caminho_pdf):
    # Abre o arquivo PDF
    doc = fitz.open(caminho_pdf)
    tem_imagem = False

    # Verifica cada página para imagens
    for pagina in doc:
        if pagina.get_images(full=True):
            tem_imagem = True
            break

    doc.close()
    return tem_imagem


def extrair_texto_pdf(caminho_pdf, caminho_saida):
    try:
        tika_parser.ServerEndpoint = 'http://localhost:9998/'
        # Ignora o proxy para localhost
        session = requests.Session()
        session.trust_env = False  # Não usa as configurações de proxy do ambiente

        # Verifica se há imagens no PDF
        if verificar_imagens_no_pdf(caminho_pdf):
            print("Imagens detectadas, realizando OCR se necessário...")
        else:
            print("Nenhuma imagem detectada, extraindo apenas o texto...")

        # Extrai o texto usando o Tika
        texto_extraido = tika_parser.from_file(caminho_pdf)
    except Exception as e:
        print(f'Erro ao processar o arquivo: {e}')

    # Salva o texto extraído em um arquivo txt
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto_extraido['content'])


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

nome_arquivo, extensao = os.path.splitext(os.path.basename(path_pdf))
nome_arquivo_txt = f"{nome_arquivo}.txt"
path_arquivo_txt = os.path.join(os.path.dirname(path_pdf), nome_arquivo_txt)

extrair_texto_pdf(path_pdf, path_arquivo_txt)
