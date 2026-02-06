# 🥗 NutriSaúde - Sistema de Agendamento de Consultas Nutricionistas

## 📋 Descrição

Aplicação web desenvolvida em Flask para divulgação e agendamento de consultas com nutricionista.  
Projeto acadêmico da disciplina **Programação Web 1** (Engenharia de Software), com foco em validações no backend, persistência em CSV (sem biblioteca externa) e páginas responsivas.

O sistema possui dois fluxos:

- **Cliente (público):** acessa o site, agenda a consulta e recebe feedback do envio.
- **Nutricionista (restrito):** acessa uma área protegida por login para visualizar e gerenciar consultas (status).

---

## 🎯 Funcionalidades

### Público (Cliente)
- ✅ Página inicial com apresentação do serviço
- ✅ Formulário de agendamento
- ✅ Validação dos dados no backend
- ✅ Salvamento em CSV (leitura/escrita manual)
- ✅ Mensagens de feedback (flash)

### Restrito (Nutricionista)
- ✅ Login (sessão)
- ✅ Área profissional com resumo das consultas por status
- ✅ Listagem de consultas (tabela)
- ✅ Atualização do status das consultas (Pendente, Confirmada, Cancelada, Concluída)
- ✅ Rotas protegidas (não acessa sem autenticação)

---

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.x
- Flask
- Jinja2 (templates)

### Frontend
- HTML5
- CSS3
- Media Queries (responsividade)

### Persistência
- CSV (manipulação manual via `open()`, `readlines()`, `write()`)

---
## Diagrama de Casos de Uso (UML)


<img width="955" height="632" alt="image" src="https://github.com/user-attachments/assets/c931f614-145b-448c-a0ab-a40904135962" />

## Projeto Arquitetural

<img width="1536" height="1024" alt="projeto arquitetural" src="https://github.com/user-attachments/assets/33ac3b00-11bb-4fbe-98fc-628edfeda4ea" />

## 📁 Estrutura do Projeto

drnutri_site/
├── app.py
├── app/
│ ├── init.py
│ └── routes.py
├── static/
│ ├── css/
│ │ └── style.css
│ └── images/
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── agendamento.html
│ ├── consultas.html
│ ├── area_profissional.html
│ └── login.html
├── data/
│ └── agendamentos.csv
└── README.md
```

## 🚀 Como Instalar e Rodar

### Pré-requisitos
- Python 3.7 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone ou baixe o projeto**
```bash
cd nutricionista_site
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python3 -m venv venv
```

3. **Ative o ambiente virtual**

No Linux/Mac:
```bash
source venv/bin/activate
```

No Windows:
```bash
venv\Scripts\activate
```

4. **Instale o Flask**
```bash
pip install flask
```

5. **Execute a aplicação**
```bash
python app.py
```

6. **Acesse no navegador**
```
http://localhost:5000
```

## 🔐 Rotas principais

- Cliente (público)

    / — Home

    /agendamento — Agendar consulta

- Nutricionista (restrito)

    /login — Login

    /logout — Sair

    /area-profissional — Dashboard do nutricionista

    /consultas — Lista de consultas

    /consultas/<id>/status — Atualiza status (POST)

## ✅ O que foi aplicado no projeto (requisitos da disciplina)

- Validações no backend (if/else) e tratamento de erros
- Leitura e escrita em CSV usando apenas funções nativas do Python
- Estruturas de repetição para listar/processar agendamentos
- Templates com herança (base.html) e renderização com Jinja2
- Formulário e tabela HTML para cadastro e visualização
- Layout responsivo com CSS e media queries
- Controle de acesso do nutricionista via sessão (login/logout)

## 🎨 Características do Design

- Layout responsivo (desktop e mobile)
- Paleta em tons de verde voltada para saúde
- Tabelas com melhor leitura (linhas alternadas) e feedback visual (hover)

## 📊 Tipos de Consulta Disponíveis

- Nutrição Esportiva
- Emagrecimento
- Reeducação Alimentar

## 🔒 Validações Implementadas

- Nome completo (mínimo 3 caracteres)
- Telefone (mínimo 10 dígitos)
- Email (formato válido)
- Data (não permite datas passadas)
- Horário (seleção obrigatória)
- Tipo de consulta (opções pré-definidas)

## 📄 Formato do CSV

O arquivo `data/agendamentos.csv` funciona como base de dados do sistema 

Formato base:

```csv
nome,telefone,email,data,horario,tipo_consulta
João Silva,(11) 98765-4321,joao@email.com,2024-12-01,09:00,Emagrecimento
```

## 👨‍💻 Autor

Projeto desenvolvido por Lucas de Moura, Vinicius e Emanuel Vitor

## 📜 Licença

Este é um projeto acadêmico de código aberto para fins educacionais.

---

**Desenvolvido com ❤️ usando Flask e Python**
