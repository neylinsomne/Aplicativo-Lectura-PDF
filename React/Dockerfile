# Usa una imagen oficial de Node.js como base
FROM node:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo package.json y package-lock.json
COPY package*.json ./

# Instala las dependencias (incluyendo Vite)
RUN npm install

# Instala Vite usando la versión más reciente disponible
RUN npm create vite@latest

# Expone el puerto en el que corre la aplicación
EXPOSE 3000

# Copia el código de la aplicación al contenedor
COPY . .

# Corre la aplicación usando Vite
CMD ["npm", "run", "dev"]
