FROM python:3.7-alpine3.8
LABEL maintainer="Thomás Marques"

WORKDIR /usr/src/app/

# Instalar dependências
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip3 install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Apenas para imagem de produção
COPY . /usr/src/app/

ENTRYPOINT ["python3", "main.py"]