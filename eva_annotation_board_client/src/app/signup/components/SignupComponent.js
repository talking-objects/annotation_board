"use client"

import { signup } from "@/app/api";
import { useUser } from "@/app/utils/hooks/useUser";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

const SignupComponent = () => {
    const { user } = useUser();
    const router = useRouter();
    const { register, handleSubmit, formState: { errors }, watch } = useForm();
    const [signupError, setSignupError] = useState("");

    useEffect(() => {
        // Redirect logged in users to home
        if (user) {
            router.push('/');
        }
    }, [user, router]);

    const onSubmit = (data) => {
        setSignupError(""); // Clear any previous error
        signup({
            username: data.username,
            password: data.password,
            key: data.key
        }).then((res) => {
            // Redirect to login after successful signup
            router.push('/login');
        }).catch((error) => {
            console.log(error);
            setSignupError("Failed to sign up. Please check your information and try again.");
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
                <h1 className="text-2xl font-bold mb-6">Sign Up</h1>
                <form onSubmit={handleSubmit(onSubmit)} className="w-full flex flex-col items-center gap-4">
                    {signupError && <span className="text-red-500 text-sm">{signupError}</span>}
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

                    <input 
                        {...register("passwordConfirm", { 
                            required: "Please confirm your password",
                            validate: (val) => {
                                if (watch('password') != val) {
                                    return "Passwords do not match";
                                }
                            }
                        })}
                        type="password" 
                        placeholder="Confirm Password" 
                        className="w-1/2 h-10 rounded-md border border-gray-300 px-3" 
                    />
                    {errors.passwordConfirm && <span className="text-red-500 text-sm">{errors.passwordConfirm.message}</span>}

                    <input 
                        {...register("key", { required: "Key is required" })}
                        type="text" 
                        placeholder="Registration Key" 
                        className="w-1/2 h-10 rounded-md border border-gray-300 px-3" 
                    />
                    {errors.key && <span className="text-red-500 text-sm">{errors.key.message}</span>}
                    
                    <button 
                        type="submit" 
                        className="w-1/2 h-10 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition-colors"
                    >
                        Sign Up
                    </button>
                    <Link href="/login" className="text-sm text-gray-500">Already have an account? Login</Link>
                </form>
            </div>
        </div>
    )
}

export default SignupComponent;