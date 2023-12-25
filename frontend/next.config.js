/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['www.camara.cl'],
    unoptimized: true,
  },
}

module.exports = nextConfig
