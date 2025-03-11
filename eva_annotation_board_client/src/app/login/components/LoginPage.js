"use client"

import { login } from "@/app/api";
import { useUser } from "@/app/utils/hooks/useUser";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

const LoginPageComponent = () => {
    const { user } = useUser();
    const router = useRouter();
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [loginError, setLoginError] = useState("");

    useEffect(() => {
        // Redirect logged in users to home
        if (user) {
            router.push('/');
        }
    }, [user, router]);

    const onSubmit = (data) => {
        setLoginError(""); // Clear any previous error
        login({
            username: data.username,
            password: data.password
        }).then((res) => {
            // Redirect to home after successful login
            router.push('/');
        }).catch((error) => {
            setLoginError("Invalid username or password. Please try again.");
        });
    }

    // Don't render anything if user is already logged in
    if (user) return null;

    return (
        <div className="w-screen h-screen flex justify-center items-center bg-gray-100">
            <div className="w-1/2 h-2/3 bg-white rounded-lg shadow-md flex flex-col items-center justify-center pb-8">
                <div className="w-1/2 h-1/2 relative ">
                    <Image src="/logo/logo.png" alt="logo" 
                        fill
                        style={{objectFit: "contain"}}
                    />
                </div>
                <h1 className="text-2xl font-bold mb-6">Login</h1>
                <form onSubmit={handleSubmit(onSubmit)} className="w-full flex flex-col items-center gap-4">
                    {loginError && <span className="text-red-500 text-sm">{loginError}</span>}
                    <input 
                        {...register("username", { required: "Username is required" })}
                        type="text" 
                        placeholder="Username" 
                        className="w-1/2 h-10 rounded-md border border-gray-300 px-3" 
                    />
                    {errors.username && <span className="text-red-500 text-sm">{errors.username.message}</span>}
                    
                    <input 
                        {...register("password", { required: "Password is required" })}
                        type="password" 
                        placeholder="Password" 
                        className="w-1/2 h-10 rounded-md border border-gray-300 px-3" 
                    />
                    {errors.password && <span className="text-red-500 text-sm">{errors.password.message}</span>}
                    
                    <button 
                        type="submit" 
                        className="w-1/2 h-10 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition-colors"
                    >
                        Login
                    </button>
                    <Link href="/signup" className="text-sm text-gray-500">Don't have an account? Sign up</Link>
                    <a href={process.env.ADMIN_URL} target="_blank" className="text-sm text-gray-500">Open Admin Panel</a>
                </form>
            </div>
        </div>
    )
}

export default LoginPageComponent;