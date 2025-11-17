# Argumento para podermos usar a mesma receita para o Master e o RegionServer
ARG HBASE_IMAGE=bde2020/hbase-master:latest

# Use a imagem base do HBase da BDE
FROM ${HBASE_IMAGE}

# --- VERSÃO CORRIGIDA ---
# Versão do Phoenix compatível com HBase 1.2.x, encontrada na sua pesquisa
ARG PHOENIX_VERSION=4.14.1-HBase-1.2

# Variáveis de ambiente para facilitar os caminhos
ENV PHOENIX_HOME /opt/phoenix
# --- URL CORRIGIDA ---
# A URL agora aponta para o diretório da versão correta
ENV PHOENIX_URL https://archive.apache.org/dist/phoenix/apache-phoenix-${PHOENIX_VERSION}/bin/apache-phoenix-${PHOENIX_VERSION}-bin.tar.gz

# Entra como root para ter permissões
USER root

# Corrige os links do repositório para a versão "Stretch" que está arquivada.
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org\/debian-security/g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list

# Adiciona a flag --allow-unauthenticated para instalar a partir de repositórios com chaves expiradas.
RUN apt-get update && apt-get install -y --allow-unauthenticated wget && rm -rf /var/lib/apt/lists/*

# Baixa, descompacta e move o Phoenix para /opt/phoenix
RUN wget --no-verbose ${PHOENIX_URL} -O /tmp/phoenix.tar.gz && \
    tar -xvf /tmp/phoenix.tar.gz -C /opt && \
    mv /opt/apache-phoenix* ${PHOENIX_HOME} && \
    rm /tmp/phoenix.tar.gz

# Copia os JARs do Phoenix para as bibliotecas do HBase
RUN cp ${PHOENIX_HOME}/phoenix-*-server.jar ${HBASE_HOME}/lib/
RUN cp ${PHOENIX_HOME}/phoenix-*-client.jar ${HBASE_HOME}/lib/