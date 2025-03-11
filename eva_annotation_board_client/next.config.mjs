
/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    output: "standalone",
    // output: 'export',
    env : {
        BASE_URL: process.env.BASE_URL,
        ADMIN_URL: process.env.ADMIN_URL,
        EVA_URL: process.env.EVA_URL,
        EVA_API_URL: process.env.EVA_API_URL,
        PROXY_HOST: process.env.PROXY_HOST,
        PROXY_PORT: process.env.PROXY_PORT,
        PROXY_PROTOCOL: process.env.PROXY_PROTOCOL
    }
};

export default nextConfig;
