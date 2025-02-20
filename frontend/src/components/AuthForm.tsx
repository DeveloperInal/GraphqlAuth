"use client"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { register, auth, logout } from "@/hooks/auth"

export default function AuthForm() {
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [username, setUsername] = useState("")

    const handleRegister = async (formData: FormData) => {
        const result = await register(formData)
        if (result && typeof result.username === 'string') {
            setIsAuthenticated(true)
            setUsername(result.username)
        }
    }

    const handleLogin = async (formData: FormData) => {
        const result = await auth(formData)
        if (result && typeof result.username === 'string') {
            setIsAuthenticated(true)
            setUsername(result.username)
        }
    }

    const handleLogout = async () => {
        await logout()
        setIsAuthenticated(false)
        setUsername("")
    }

    if (isAuthenticated) {
        return (
            <Card className="w-[350px]">
                <CardHeader>
                    <CardTitle>Welcome, {username}!</CardTitle>
                    <CardDescription>You are now logged in.</CardDescription>
                </CardHeader>
                <CardFooter>
                    <Button onClick={handleLogout} className="w-full">
                        Logout
                    </Button>
                </CardFooter>
            </Card>
        )
    }

    return (
        <Tabs defaultValue="login" className="w-[350px]">
            <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="login">Login</TabsTrigger>
                <TabsTrigger value="register">Register</TabsTrigger>
            </TabsList>
            <TabsContent value="login">
                <Card>
                    <CardHeader>
                        <CardTitle>Login</CardTitle>
                        <CardDescription>Enter your credentials to login.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        <form action={handleLogin}>
                            <div className="space-y-1">
                                <Label htmlFor="login-username">Username</Label>
                                <Input id="login-username" name="username" required />
                            </div>
                            <div className="space-y-1">
                                <Label htmlFor="login-email">Email</Label>
                                <Input id="login-email" name="email" type="email" required />
                            </div>
                            <div className="space-y-0">
                                <Label htmlFor="login-password">Password</Label>
                                <Input id="login-password" name="password" type="password" required />
                            </div>
                            <Button type="submit" className="w-full mt-4">
                                Login
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            </TabsContent>
            <TabsContent value="register">
                <Card>
                    <CardHeader>
                        <CardTitle>Register</CardTitle>
                        <CardDescription>Create a new account.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        <form action={handleRegister}>
                            <div className="space-y-1">
                                <Label htmlFor="login-username">Username</Label>
                                <Input id="login-username" name="username" required />
                            </div>
                            <div className="space-y-1">
                                <Label htmlFor="login-email">Email</Label>
                                <Input id="login-email" name="email" type="email" required />
                            </div>
                            <div className="space-y-0">
                                <Label htmlFor="login-password">Password</Label>
                                <Input id="login-password" name="password" type="password" required />
                            </div>
                            <Button type="submit" className="w-full mt-4">
                                Register
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            </TabsContent>
        </Tabs>
    )
}
