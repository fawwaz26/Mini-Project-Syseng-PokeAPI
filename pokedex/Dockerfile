# Fase build: Menggunakan image Node.js untuk membangun kode sumber ReactJS
FROM node:14-alpine as build

# Menetapkan direktori kerja
WORKDIR /app

# Menyalin package.json dan package-lock.json
COPY package.json /app/

# Menginstal dependencies
RUN npm install

# Menyalin kode sumber ReactJS ke dalam container
COPY . /app

RUN chmod +x node_modules/.bin/react-scripts

# Membangun aplikasi untuk produksi
RUN npm run build

# Fase run: Menggunakan Nginx untuk melayani aplikasi ReactJS
FROM nginx:alpine

# Menyalin hasil build dari fase sebelumnya ke direktori yang dituju Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Menginformasikan Docker bahwa container mendengarkan pada port 80
EXPOSE 80
