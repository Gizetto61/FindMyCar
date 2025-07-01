# FindMyCar

Projeto do 4° ano no Curso Técnico em Informática Integrado ao Ensino Médio pelo IFSP(SPO)/PDS <br>
Aplicação Web para recomendação do carro ideal!

# Manual de Execução

Este repositório contém um projeto desenvolvido com **Flask** como back-end. Siga o passo a passo abaixo para configurar o ambiente e rodar o sistema localmente.

---

## ⚙️ Requisitos

- [Python](https://www.python.org/) instalado (recomenda-se a versão 3.13)

---

## 🚀 Passo a Passo para Executar o Projeto

### 1. Verificar se o Python e o `pip` estão funcionando

Abra o terminal (CMD, PowerShell ou outro) e digite:

```bash
python --version
pip --version
```

### 2. Ative o ambiente virtual dessa maneira
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Baixar as dependências
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

### 4. Executar o projeto
Com tudo instalado, você pode rodar o servidor Flask com um dos seguintes comandos:
```bash
python app.py
```
ou
```bash
flask --app app run
```
