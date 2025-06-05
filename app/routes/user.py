from app import app
from starlette import status
from starlette.responses import Response

from app.models import User, SessionDep


@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.get("/user")
async def get(session: SessionDep):
    return session.exec(select(User)).all()


@app.put("/user")
async def update_item_by_id(user_id: int, new: User, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    user.content = new.content
    session.commit()

    return {"new_content": new.content}


@app.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_by_id(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(user)

    return None
