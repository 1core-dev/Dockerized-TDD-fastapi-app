from fastapi import APIRouter, HTTPException
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
        raise HTTPException(status_code=404, detail="Note not found")
    return note
