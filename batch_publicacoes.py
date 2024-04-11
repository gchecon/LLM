import requests
from bs4 import BeautifulSoup
from classes import EnvVars, EnvVarsLoadError, EnvVarNotFoundError
import os
import io
from zipfile import ZipFile


def baixar_pdf(url_inner, nome_arquivo_inner):
    response_inner = requests.get(url_inner, stream=True)
    with open(nome_arquivo_inner, "wb") as f:
        for chunk in response_inner.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def baixar_txt(texto_inner, nome_arquivo_inner):
    with open(nome_arquivo_inner, "w", encoding="utf-8") as f:
        f.write(str(texto_inner))


def carga_url(url_entrada):
    response = requests.get(url_entrada)
    soup_exit = BeautifulSoup(response.content, "html.parser")
    return soup_exit


def analisa_extensao(url_arquivo):
    if not url_arquivo.endswith('.pdf') and not url_arquivo.endswith('.zip'):
        raise ValueError('Link inválido: a URL deve terminar em .pdf ou .zip')
    if url_arquivo.endswith('.pdf'):
        nome_arquivo = url_arquivo.split("/")[-1]
        baixar_pdf(url_arquivo, nome_arquivo)
        return
    resposta = requests.get(url_arquivo)
    with io.BytesIO(resposta.content) as arquivo_zip:
        with ZipFile(arquivo_zip) as var_zip:
            # Lista para armazenar nomes dos arquivos extraídos
            nomes_arquivos = []
            for nome in var_zip.namelist():
                # Ignora pastas
                if not nome.endswith('/'):
                    nomes_arquivos.append(nome)
                    # Extrai o arquivo em memória
                    var_zip.extract(nome)
                    print(f'Gravou arquivo {nome} zipado')


def extrair_informacoes(url_inner):
    soup = carga_url(url_inner)

    # Verificar a última página para o loop
    li = soup.find("li", class_="pager__item pager__item--last")
    a = li.find('a')
    href = a.get('href')
    numero_pagina_final = href.split("=")[1]
    pagina_final = int(numero_pagina_final)
    pagina = 0

    while True:
        # Percorrer as publicações
        print(f'Processando página {pagina}')
        for publicacao in soup.find_all("div", class_="publicacao"):
            # Obter link da publicação
            link_publicacao = publicacao.find("a").get("href")
            soup_inner = carga_url(link_publicacao)

            # Verificar se existe PDF
            imagem = soup_inner.find("div", class_="publicacao_imagem")
            if imagem:
                # Baixar PDF
                if imagem.find("a") is not None:
                    link_pdf = imagem.find("a").get("href")
                    analisa_extensao(link_pdf)
                else:
                    # Baixar TXT
                    texto = soup_inner.find("div", class_="publicacao_ementa")
                    if texto is not None:
                        nome_arquivo = f"{link_publicacao.split('/')[-1]}.txt"
                        baixar_txt(texto, nome_arquivo)
        pagina += 1
        if pagina > pagina_final:
            break
        print(url_inner + "?page={}".format(pagina))
        soup = carga_url(url_inner + "?page={}".format(pagina))


if __name__ == "__main__":

    env = EnvVars()

    try:
        url = env.get('URL_BASE')
        var_dir = env.get('DIR_BASE')
    except EnvVarsLoadError as e:
        print(f"Erro ao carregar variáveis de ambiente: {e}")
        exit(1)
    except EnvVarNotFoundError as e:
        print(f"Erro: {e}")
        exit(1)

    os.makedirs(var_dir + "/downloads", exist_ok=True)
    os.chdir(var_dir + "/downloads")
    extrair_informacoes(url)
