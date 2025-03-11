import { getMe } from "@/app/api"
import { useQuery } from "@tanstack/react-query"

export const useUser = () => {
    const {isLoading, data, isError} = useQuery({
        queryKey: ["me"],
        queryFn: getMe,
        retry: false,    
        refetchOnWindowFocus: false
    });

    return {
        userLoading: isLoading,
        user: data,
        isLoggedIn: !isError
    }
}