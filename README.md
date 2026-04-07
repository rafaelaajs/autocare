# 🚗 AutoCare

Sistema web para controle de manutenção de veículos.

👉 Acesse o projeto online:
https://autocare-em9w.onrender.com/

---

## 📌 Sobre o projeto

O AutoCare é uma aplicação desenvolvida em Django para ajudar usuários a:

* Controlar manutenções do veículo
* Receber alertas de manutenção
* Visualizar histórico completo
* Evitar atrasos em revisões importantes

---

## ⚙️ Funcionalidades

* 🚗 Cadastro de veículos
* 🔧 Registro de manutenções
* 📊 Histórico de manutenção
* 🚨 Sistema de alertas (7 dias antes, no dia e atrasado)
* ✏️ Edição e exclusão de manutenções
* 🔐 Autenticação de usuários

---

## 🛠️ Tecnologias utilizadas

* Python
* Django
* SQLite
* HTML / CSS
* Gunicorn
* Render (deploy)

---

## 🚀 Como rodar o projeto localmente

### 1. Clonar repositório

```
git clone https://github.com/rafaelaajs/autocare.git
cd autocare
```

---

### 2. Criar ambiente virtual

```
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. Instalar dependências

```
pip install -r requirements.txt
```

---

### 4. Rodar migrações

```
python manage.py migrate
```

---

### 5. Executar servidor

```
python manage.py runserver
```

---

## 📧 Configuração de email

Para envio de alertas, configure variáveis de ambiente:

```
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app
```

---

## 📦 Deploy

O projeto está hospedado no Render.

---

## 📌 Próximas melhorias

* Melhorar layout e templates
* Adicionar funcionalidades conforme feedbacks de ususários  

---

## 👩‍💻 Autora

Desenvolvido por Rafaela Silva 🚀
