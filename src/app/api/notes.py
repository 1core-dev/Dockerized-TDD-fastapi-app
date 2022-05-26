from fastapi import APIRouter, HTTPException
from typing import List

from fastapi import Response
from starlette import status

from app.api import crud
from app.api.models import NoteSchema, NoteDB

router = APIRouter()


@router.post('/', response_model=NoteDB, status_code=status.HTTP_201_CREATED)
async def create_note(payoload: NoteSchema):
    note_id = await crud.post(payoload)

    response_object = {
        "id": note_id,
        "title": payoload.title,
        "description": payoload.description,
    }
    return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int):
    note = await crud.get(id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note


@router.get("/", response_model=list[NoteDB])
async def read_all_notes():
    return await crud.get_all()


@router.put("/{id}/", response_model=NoteDB)
async def udpade_note(id: int, payload: NoteSchema):
    note = crud.get(id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    note_id = await crud.put(id, payload)
    response_object = {
        "id": note_id,
        "payload": payload.title,
        "description": payload.description
    }
    return response_object


@router.delete("/{id}/")
async def delete(id: int):
    note = await crud.get(id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    await crud.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

