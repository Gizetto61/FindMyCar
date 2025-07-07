# FindMyCar

Projeto do 4° ano no Curso Técnico em Informática Integrado ao Ensino Médio pelo IFSP(SPO)/PDS <br>
Aplicação Web para recomendação do carro ideal!

# Manual de Execução

Este repositório contém um projeto desenvolvido com **Flask** como back-end. Siga o passo a passo abaixo para configurar o ambiente e rodar o sistema localmente.

---

## ⚙️ Requisitos

- [Python](https://www.python.org/) instalado (recomenda-se a versão 3.13)
- [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) instalado no seu sistema

---

## 🛢️ Instalando o MySQL

1. Acesse o site oficial do MySQL:  
   👉 [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)

2. Faça o download da versão compatível com o seu sistema operacional.

3. Após instalar, certifique-se de que o serviço do MySQL está em execução.

---


## 🚀 Passo a Passo para Executar o Projeto

### 1. Verificar se o Python e o `pip` estão funcionando

Abra o terminal (CMD, PowerShell ou outro) e digite:

```bash
python --version
pip --version
```

### 2. Clone o repositório do github
```bash
git clone https://github.com/Gizetto61/FindMyCar.git
cd findmycar
```

### 3. Ative o ambiente virtual dessa maneira
```bash
python -m venv venv
venv\Scripts\activate
```
Caso de erro ao fazer o comando acima seguir essa resposta do stackoverflow:
[Erro script](https://pt.stackoverflow.com/questions/220078/o-que-significa-o-erro-execu%C3%A7%C3%A3o-de-scripts-foi-desabilitada-neste-sistema)
### 4. Baixar as dependências
Dentro do ambiente virtual digitar estes comandos um por um:
```bash
pip install flask
```
```bash
pip install mysql-connector-python
```
```bash
pip install requests
```

### 5. Executar o projeto
Com tudo instalado, você pode rodar o servidor Flask com um dos seguintes comandos:
```bash
python app.py
```
ou
```bash
flask --app app run
```
