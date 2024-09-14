![ETL BACKEND](https://ibb.co/hDfBMjm)
https://ibb.co/hDfBMjm

Aplicativo web que lee ticketes aereos, les hace un pipeline y los mete en una base relacional


Después del ETL vamos a ver el proceso de conexión entre Backend y Frontend

Cómo iniciarlo?
Primero, debes tener docker a la mano para poder usar las imagenes:

docker-compose up -d

despues dirijete a la carpeta REACT/mantis
npm run dev

ya con ello puedes correr el aplicativo en http://localhost:5173

recuerta correr el backend:
python main.py

Y ya podras hacer uso de todos los servicios.
