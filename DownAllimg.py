import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Solicita a URL do site ao usuário
site_url = input("Digite a URL do site que você deseja baixar as imagens: ")

# Diretório onde as imagens serão salvas
download_dir = "imagens"

# Verifique se o diretório de download existe, caso contrário, crie-o
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Faça uma solicitação HTTP para a página do site
response = requests.get(site_url)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Parseie o conteúdo da página com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontre todas as tags de imagem na página
    img_tags = soup.find_all('img')

    # Percorra todas as tags de imagem e faça o download das imagens
    for img_tag in img_tags:
        # Obtenha o URL da imagem
        img_url = img_tag.get('src')

        # Verifique se o URL da imagem é absoluto ou relativo e construa o URL completo
        if img_url:
            img_url = urljoin(site_url, img_url)

            # Extraia o nome do arquivo da URL da imagem
            img_filename = os.path.basename(urlparse(img_url).path)

            # Faça o download da imagem e salve-a no diretório de download
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                with open(os.path.join(download_dir, img_filename), 'wb') as img_file:
                    img_file.write(img_response.content)
                    print(f"Imagem '{img_filename}' baixada com sucesso!")

else:
    print(f"Falha ao acessar o site. Código de status: {response.status_code}")
