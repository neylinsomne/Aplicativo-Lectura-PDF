from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import pipeline
from BD.conectar import ret_data_url
from databases import Database
import asyncpg

app = FastAPI()

# Get the database URL
db_url = ret_data_url()

# Create the database instance
database = Database(db_url)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_FOLDER = 'assets/Tiquetes'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    try:

        result = pipeline.put_pipeline(file_path)
        
        
        return JSONResponse(content={
            "message": "File uploaded and processed successfully",
            "result": result
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/api/graph-data")
async def get_graph_data():
    # This is a placeholder. You'll need to implement your actual data fetching logic here.
    # This might involve querying your database or processing stored results.
    return [
        {"name": "Page A", "value": 400},
        {"name": "Page B", "value": 300},
        {"name": "Page C", "value": 200},
        {"name": "Page D", "value": 278},
        {"name": "Page E", "value": 189},
    ]

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/api/aerolineas-pasajeros")
async def get_aerolineas_pasajeros():
    query = """
    SELECT a.nombre_aerolinea, COUNT(DISTINCT p.id_cliente) as total_pasajeros
    FROM "Aerolineas" a
    JOIN "Pasaje" p ON a.id = p.id_aerolinea
    GROUP BY a.nombre_aerolinea
    """
    results = await database.fetch_all(query)
    return [dict(result) for result in results]

@app.get("/api/vuelos-por-mes")
async def get_vuelos_por_mes():
    query = """
    SELECT DATE_TRUNC('month', fecha_origen) as mes, COUNT(*) as total_vuelos
    FROM "Vuelo"
    GROUP BY DATE_TRUNC('month', fecha_origen)
    ORDER BY mes
    """
    results = await database.fetch_all(query)
    return [dict(result) for result in results]

@app.get("/api/destinos-populares")
async def get_destinos_populares():
    query = """
    SELECT destino, COUNT(*) as total_vuelos
    FROM "Vuelo"
    GROUP BY destino
    ORDER BY total_vuelos DESC
    LIMIT 5
    """
    results = await database.fetch_all(query)
    return [dict(result) for result in results]

@app.get("/api/ocupacion-vuelos")
async def get_ocupacion_vuelos():
    query = """
    SELECT v.id, v.origen, v.destino, COUNT(p.codigo_reserva) as pasajeros
    FROM "Vuelo" v
    LEFT JOIN "Pasaje" p ON v.id = p.id_vuelo
    GROUP BY v.id, v.origen, v.destino
    ORDER BY pasajeros DESC
    LIMIT 10
    """
    results = await database.fetch_all(query)
    return [dict(result) for result in results]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)