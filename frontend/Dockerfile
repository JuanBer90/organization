# Usa la imagen base de Node.js
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia package.json y package-lock.json
COPY package.json package-lock.json ./

# Instala las dependencias de desarrollo y producción
RUN npm install --include=dev

# Copia el resto del código fuente
COPY . .

# Expone el puerto donde servirá la app (puedes cambiar este puerto si lo deseas)
EXPOSE 3000

# Ejecuta TypeScript y luego ejecuta la aplicación con Node.js
CMD ["npm", "run", "build", "&&", "node", "dist/index.js"]
