import requests
from bs4 import BeautifulSoup
from classes import EnvVars, EnvVarsLoadError, EnvVarNotFoundError


def baixar_pdf(url_inner, nome_arquivo_inner):
    response_inner = requests.get(url_inner, stream=True)
    with open(nome_arquivo_inner, "wb") as f:
        for chunk in response_inner.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def baixar_txt(texto_inner, nome_arquivo_inner):
    with open(nome_arquivo_inner, "w", encoding="utf-8") as f:
        f.write(texto_inner)


env = EnvVars()

try:
    url = env.get('URL_BASE')
except EnvVarsLoadError as e:
    print(f"Erro ao carregar variáveis de ambiente: {e}")
    exit(1)
except EnvVarNotFoundError as e:
    print(f"Erro: {e}")
    exit(1)

response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")

# Percorrer as publicações
for publicacao in soup.find_all("div", class_="publicacao"):
    # Obter link da publicação
    link_publicacao = publicacao.find("a").get("href")

    # Verificar se existe PDF
    imagem = publicacao.find("div", class_="publicacao_imagem")
    if imagem:
        # Baixar PDF
        link_pdf = imagem.find("a").get("href")
        nome_arquivo = link_pdf.split("/")[-1]
        baixar_pdf(link_pdf, nome_arquivo)
    else:
        # Baixar TXT
        texto = publicacao.find("div", class_="publicacao_ementa").text
        nome_arquivo = f"{link_publicacao.split('/')[-1]}.txt"
        baixar_txt(texto, nome_arquivo)
