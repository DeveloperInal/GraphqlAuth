# Проект авторизации с использованием GraphQL

## Описание
Этот проект реализует систему авторизации пользователей с использованием **GraphQL**, **FastAPI**, **Next.js** и **TypeScript**. Данный стек технологий позволяет создать современное, эффективное и масштабируемое решение для управления пользователями.

## Стек технологий
- **Backend:** FastAPI, Strawberry GraphQL, SQLAlchemy, PostgreSQL, Redis, bcrypt, JWT
- **Frontend:** Next.js, TypeScript, React, TailwindCSS
- **База данных:** PostgreSQL

## Функциональность
- Регистрация пользователя через GraphQL
- Аутентификация пользователя через GraphQL
- Выход из системы с удалением токена
- Хранение пароля в зашифрованном виде (bcrypt)
- Использование JWT-токенов для аутентификации
- Обновление и валидация данных пользователя

## Установка и запуск

### 1. Клонирование репозитория
```bash
  git clone https://github.com/your-repo/auth-graphql.git
  cd auth-graphql
```
### 2. Запуск проекта
```bash
docker-compose up -d
```

## GraphQL-запросы
### Регистрация пользователя
```graphql
mutation RegUser($username: String!, $password: String!, $email: String!) {
  registerUser(username: $username, password: $password, email: $email) {
    userId
    message
    token {
      accessToken
    }
  }
}
```

### Аутентификация пользователя
```graphql
mutation AuthUser($username: String!, $password: String!) {
  authUser(username: $username, password: $password) {
    userId
    message
    token {
      accessToken
    }
  }
}
```

### Выход из системы
```graphql
mutation LogoutUser {
  logoutUser {
    message
  }
}
```

## Дополнительная информация
- Реализована защита API с использованием **JWT-токенов**
- Логирование действий пользователей через **Loguru**
- Пароли хранятся в безопасном виде с использованием **bcrypt**
