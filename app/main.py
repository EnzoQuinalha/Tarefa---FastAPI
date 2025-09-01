from fastapi import FastAPI
from pydantic import validator
from model.db import Database
from routes.movie_routes import router as movie_router

app = FastAPI()
db = Database()

# Validação extra para Index
@validator('searchTerm', 'poster_url', pre=True, allow_reuse=True)
def not_empty(v, field):
	if v is None or str(v).strip() == "":
		raise ValueError(f"{field.name} não pode ser vazio ou nulo.")
	return v

@app.on_event("startup")
def startup_event():
	db.conectar()

@app.on_event("shutdown")
def shutdown_event():
	db.desconectar()

# Inclui as rotas de filmes para aparecerem na documentação
app.include_router(movie_router)

