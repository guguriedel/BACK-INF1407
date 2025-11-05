# Acervo de Filmes - Backend API

Sistema de gerenciamento de filmes assistidos desenvolvido com Django REST Framework.

## 👥 Componentes do Grupo

- Gustavo Riedel - 2210375
- Rodrigo Kauer - 211

## 📝 Descrição do Projeto

O Acervo de Filmes Backend é uma API REST desenvolvida em Django que permite aos usuários gerenciar sua coleção pessoal de filmes assistidos. O sistema oferece funcionalidades completas de autenticação, gerenciamento de usuários e operações CRUD para filmes.

### Escopo do Sistema

- **Autenticação**: Sistema de login com tokens
- **Gerenciamento de Usuários**: Registro, troca de senha e recuperação de senha
- **CRUD de Filmes**: Criar, listar, visualizar, editar e deletar filmes
- **Isolamento de Dados**: Cada usuário visualiza apenas seus próprios filmes
- **Documentação Automática**: Interface Swagger para testar todos os endpoints

## 🚀 Tecnologias Utilizadas

### Backend
- **Python** 3.9+
- **Django** 4.2.25
- **Django REST Framework** 3.16.1
- **drf-yasg** 1.21.11 (Documentação Swagger/OpenAPI)
- **django-cors-headers** 4.9.0 (CORS)
- **SQLite3** (Banco de dados)

## 📦 Como Instalar

### Pré-requisitos

- Python 3.9 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passo 1: Clone o repositório

```bash
git clone https://github.com/guguriedel/BACK-INF1407.git
cd AcervoAPI
```

### Passo 2: Crie e ative um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instale as dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configure o banco de dados

```bash
cd AcervoAPI
python manage.py makemigrations
python manage.py migrate
```

### Passo 5: (Opcional) Crie um superusuário para acessar o admin

```bash
python manage.py createsuperuser
```

Siga as instruções na tela para criar username, email e senha.

### Passo 6: Rode o servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: **http://127.0.0.1:8000/**

## 🌐 Links

- **API Base**: http://127.0.0.1:8000/
- **Documentação Swagger**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **Admin Django**: http://127.0.0.1:8000/admin/
- **Frontend**: [URL do Frontend quando publicado]

## 📖 Manual do Usuário (API)

### Endpoints Disponíveis

#### 1. Autenticação

**Login**
```
POST /filmes/login/
Body: {
    "username": "usuario",
    "password": "senha"
}
Resposta: {
    "token": "token"
}
```

**Registro de Novo Usuário**
```
POST /filmes/register/
Body: {
    "username": "novo_usuario",
    "email": "email@example.com",
    "password": "senha_forte_123",
    "password_confirm": "senha_forte_123",
    "first_name": "Nome (opcional)",
    "last_name": "Sobrenome (opcional)"
}
```

#### 2. Gerenciamento de Senha

**Trocar Senha (Autenticado)**
```
POST /filmes/change-password/
Headers: Authorization: Token SEU_TOKEN
Body: {
    "old_password": "senha_atual",
    "new_password": "nova_senha_123",
    "new_password_confirm": "nova_senha_123"
}
```

**Esqueci Minha Senha**
```
POST /filmes/forgot-password/
Body: {
    "email": "seu@email.com"
}
```

**Reset de Senha**
```
POST /filmes/reset-password/
Body: {
    "token": "token_recebido",
    "new_password": "nova_senha_123",
    "new_password_confirm": "nova_senha_123"
}
```

#### 3. CRUD de Filmes (Todos requerem autenticação)

**Listar Filmes do Usuário**
```
GET /filmes/
Headers: Authorization: Token SEU_TOKEN
```

**Criar Novo Filme**
```
POST /filmes/
Headers: Authorization: Token 
Body: {
    "nome": "Matrix",
    "data_visto": "2024-01-15",
    "nota": 9.5,
    "duracao_min": 136
}
```

**Ver Detalhes de um Filme**
```
GET /filmes/{id}/
Headers: Authorization: Token 
```

**Atualizar Filme**
```
PUT /filmes/{id}/
Headers: Authorization: Token 
Body: {
    "nome": "Matrix Reloaded",
    "data_visto": "2024-01-16",
    "nota": 8.5,
    "duracao_min": 138
}
```

**Deletar Filme**
```
DELETE /filmes/{id}/
Headers: Authorization: Token
```

### Como Usar a API (Passo a Passo)

1. **Registre-se**: Use o endpoint `/filmes/register/` ou crie um usuário pelo admin
2. **Faça Login**: Use `/filmes/login/` com suas credenciais para receber um token
3. **Guarde o Token**: Todas as requisições seguintes precisam do header `Authorization: Token SEU_TOKEN`
4. **Adicione Filmes**: Use `POST /filmes/` para adicionar filmes à sua coleção
5. **Gerencie**: Liste, edite ou delete seus filmes usando os endpoints CRUD



## ✅ O Que Funcionou

### Funcionalidades Testadas e Aprovadas

1. ✅ **Autenticação com Token**
   - Login funciona corretamente
   - Token é gerado e pode ser usado em requisições subsequentes

2. ✅ **Registro de Usuários**
   - Novos usuários podem se cadastrar
   - Validação de senha forte implementada
   - Email é obrigatório

3. ✅ **Gerenciamento de Senha**
   - Troca de senha para usuários autenticados funciona
   - Sistema de reset de senha com tokens temporários funciona
   - Tokens expiram após 1 hora
   - Tokens só podem ser usados uma vez

4. ✅ **CRUD Completo de Filmes**
   - CREATE: Adicionar novos filmes funciona
   - READ: Listar e visualizar filmes funciona
   - UPDATE: Editar filmes funciona
   - DELETE: Remover filmes funciona

5. ✅ **Isolamento de Dados por Usuário**
   - Cada usuário vê apenas seus próprios filmes
   - Não é possível acessar filmes de outros usuários

6. ✅ **Swagger/OpenAPI**
   - Documentação automática gerada corretamente
   - Todos os endpoints estão documentados
   - Interface interativa permite testar a API

7. ✅ **Validações**
   - Validação de campos obrigatórios
   - Validação de formato de email
   - Validação de força de senha
   - Validação de tipos de dados (número, data, etc.)

8. ✅ **CORS Configurado**
   - API aceita requisições de origens diferentes
   - Frontend pode comunicar com o backend

## ❌ O Que Não Funcionou


### Limitações Conhecidas

1. **Sistema de Email**: O reset de senha retorna o token na resposta HTTP em vez de enviar por email (requer configuração de servidor SMTP para produção)

2. **Banco de Dados**: SQLite é usado para desenvolvimento, mas para produção deveria ser PostgreSQL ou MySQL

3. **Segurança**:
   - SECRET_KEY está exposta no código (deveria usar variáveis de ambiente)
   - DEBUG=True (deve ser False em produção)

## 🔧 Configuração para Produção

Para publicar em produção, você precisa:

1. Configurar variáveis de ambiente para dados sensíveis
2. Mudar DEBUG=False no settings.py
3. Configurar ALLOWED_HOSTS
4. Usar PostgreSQL ou MySQL
5. Configurar servidor de email para reset de senha
6. Configurar servidor WSGI (Gunicorn) ou ASGI
7. Configurar arquivos estáticos (collectstatic)

## 🐛 Troubleshooting

**Erro: "ModuleNotFoundError: No module named 'django'"**
- Solução: Ative o ambiente virtual com `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)

**Erro: "No such table: filmes_filme"**
- Solução: Rode `python manage.py migrate`

**Erro de CORS no frontend**
- Solução: Verifique se django-cors-headers está instalado e configurado no settings.py

## 📚 Estrutura do Projeto

```
AcervoAPI/
├── AcervoAPI/              # Projeto Django principal
│   ├── settings.py         # Configurações do Django
│   ├── urls.py            # URLs principais (inclui Swagger)
│   └── wsgi.py            # Arquivo WSGI
├── filmes/                # App Django de filmes
│   ├── migrations/        # Migrações do banco
│   ├── models.py          # Modelos (Filme, PasswordResetToken)
│   ├── serializers.py     # Serializers do DRF
│   ├── views.py           # Views/Endpoints da API
│   ├── urls.py            # URLs do app
│   └── admin.py           # Configuração do admin
├── db.sqlite3             # Banco de dados SQLite
├── manage.py              # Script de gerenciamento Django
└── requirements.txt       # Dependências Python
```



---

**Desenvolvido como parte do trabalho de Programação para Web - PUC 2025/2**
