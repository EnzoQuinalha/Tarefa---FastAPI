
from fastapi import APIRouter, HTTPException
from typing import List
from model.models import Index
from model.db import Database

router = APIRouter()

@router.get("/movies", response_model=List[Index])
def list_movies():
	db = Database()
	db.conectar()
	db.cursor.execute("SELECT * FROM `index`")
	result = db.cursor.fetchall()
	db.desconectar()
	return [Index(**row) for row in result]

@router.get("/movies/{id}", response_model=Index)
def get_movie(id: int):
	db = Database()
	db.conectar()
	db.cursor.execute("SELECT * FROM `index` WHERE idIndex=%s", (id,))
	row = db.cursor.fetchone()
	db.desconectar()
	if not row:
		raise HTTPException(status_code=404, detail="Filme não encontrado")
	return Index(**row)

@router.post("/movies", response_model=Index)
def create_movie(movie: Index):
	if movie.searchTerm.strip() == "" or movie.poster_url.strip() == "":
		raise HTTPException(status_code=422, detail="searchTerm e poster_url não podem ser vazios.")
	db = Database()
	db.conectar()
	db.cursor.execute(
		"INSERT INTO `index` (searchTerm, count, poster_url, movie_id) VALUES (%s, %s, %s, %s)",
		(movie.searchTerm, movie.count, movie.poster_url, movie.movie_id)
	)
	db.connection.commit()
	new_id = db.cursor.lastrowid
	db.cursor.execute("SELECT * FROM `index` WHERE idIndex=%s", (new_id,))
	row = db.cursor.fetchone()
	db.desconectar()
	return Index(**row)

@router.put("/movies/{id}", response_model=Index)
def update_movie(id: int, movie: Index):
	if movie.searchTerm.strip() == "" or movie.poster_url.strip() == "":
		raise HTTPException(status_code=422, detail="searchTerm e poster_url não podem ser vazios.")
	db = Database()
	db.conectar()
	db.cursor.execute("SELECT * FROM `index` WHERE idIndex=%s", (id,))
	if not db.cursor.fetchone():
		db.desconectar()
		raise HTTPException(status_code=404, detail="Filme não encontrado")
	db.cursor.execute(
		"UPDATE `index` SET searchTerm=%s, count=%s, poster_url=%s, movie_id=%s WHERE idIndex=%s",
		(movie.searchTerm, movie.count, movie.poster_url, movie.movie_id, id)
	)
	db.connection.commit()
	db.cursor.execute("SELECT * FROM `index` WHERE idIndex=%s", (id,))
	row = db.cursor.fetchone()
	db.desconectar()
	return Index(**row)

@router.delete("/movies/{id}")
def delete_movie(id: int):
	db = Database()
	db.conectar()
	db.cursor.execute("SELECT * FROM `index` WHERE idIndex=%s", (id,))
	if not db.cursor.fetchone():
		db.desconectar()
		raise HTTPException(status_code=404, detail="Filme não encontrado")
	db.cursor.execute("DELETE FROM `index` WHERE idIndex=%s", (id,))
	db.connection.commit()
	db.desconectar()
	return {"detail": "Filme removido"}



