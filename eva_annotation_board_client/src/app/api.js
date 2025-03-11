import axios from "axios";
import Cookies from "js-cookie";


const instance = axios.create({
    baseURL: process.env.NODE_ENV === 'development' 
    ? "http://127.0.0.1:8000/api/v1/"
    : process.env.EVA_API_URL,
    // ...(process.env.NODE_ENV === 'production' && {
    //     proxy: {
    //         host: process.env.PROXY_HOST,
    //         port: process.env.PROXY_PORT,
    //         protocol: process.env.PROXY_PROTOCOL
    //     }
    // }),
    withCredentials: true
})


export const login = ({username, password}) => {
    return instance.post(
        "users/log-in",
        {username, password},
        {
            headers: {
               
                "X-CSRFToken": Cookies.get("csrftoken") || ""
            }
        }
    ).then((response) => response.data)
}   

export const signup = ({username, password, key}) => {
    return instance.post("users/", {username, password, key}).then((response) => response.data)
}   

export const getMe = () =>
    instance.get(`users/me`).then((response) => response.data);

export const getVideos = () => instance.get(`videos/`).then((response) => response.data);
  
export const logout = () => {
    return instance.post(
        "users/log-out",
        null,
        {
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken") || ""
            }
        }
    ).then((response) => response.data)
}

export const uploadVideo = (variable) => {
    return instance.post(`videos/`, variable, {
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken") || ""
        }
    }).then((response) => response.data);
};