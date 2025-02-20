"use server"

import { cookies } from "next/headers"

const GRAPHQL_ENDPOINT = "http://0.0.0.0:8000/auth"

async function fetchGraphQL(query: any, variables = {}) {
    const response = await fetch(GRAPHQL_ENDPOINT, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query, variables }),
    })

    const result = await response.json()
    if (result.errors) {
        throw new Error(result.errors[0].message)
    }
    return result.data
}

export async function register(formData: FormData) {
    const username = formData.get("username")
    const password = formData.get("password")
    const email = formData.get("email")

    const query = `
    mutation RegisterUser($username: String!, $password: String!, $email: String!) {
      registerUser(username: $username, password: $password, email: $email) {
        userId,
        message,
        token {
          accessToken
        }
      }
    }`

    const data = await fetchGraphQL(query, { username, password, email })

    if (data.registerUser.success) {
        const cookieStore = await cookies()
        cookieStore.set("access_token", data.registerUser.token.accessToken, { httpOnly: true })
        cookieStore.set("user_id", data.registerUser.userId, { httpOnly: true })
    }

    return { message: data.registerUser.message, username }
}

export async function auth(formData: FormData) {
    const username = formData.get("username")
    const password = formData.get("password")
    const email = formData.get("email")

    const query = `
    mutation AuthUser($username: String!, $password: String!, $email: String!) {
      authUser(username: $username, password: $password, email: $email) {
        userId,
        message,
        token {
          accessToken
        }
      }
    }`

    const data = await fetchGraphQL(query, { username, password, email })

    if (data.authUser.success) {
        const cookieStore = await cookies()
        cookieStore.set("access_token", data.authUser.token.accessToken, { httpOnly: true })
        cookieStore.set("user_id", data.authUser.userId, { httpOnly: true })
    }

    return { message: data.authUser.message, username }
}

export async function logout() {
    const query = `
    mutation LogoutUser {
      logoutUser {
        message
      }
    }`

    const data = await fetchGraphQL(query)

    if (data.logoutUser.success) {
        const cookieStore = await cookies()
        cookieStore.delete("access_token")
        cookieStore.delete("user_id")
    }

    return { message: data.logoutUser.message }
}
