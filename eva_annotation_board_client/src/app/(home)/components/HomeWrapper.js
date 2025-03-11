"use client"

import { useUser } from "@/app/utils/hooks/useUser";
import { logout } from "@/app/api";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import TWrapper from "./TWrapper";

const HomeWrapper = ({pandora}) => {
    const router = useRouter();
    const {userLoading, user, isLoggedIn} = useUser()
  
    const onLogout = () => {
        logout().then((res) => {
            window.location.reload()
        })
    }

    useEffect(() => {
        console.log(pandora)
        if (!isLoggedIn || !user) {
            router.push('/login');  // Redirect to login page if not logged in
        }
    }, [isLoggedIn, user, router]);

    if(userLoading) {
        return null;
    }

    return (
        <TWrapper pandora={pandora.data.items} />
    )
}

export default HomeWrapper;