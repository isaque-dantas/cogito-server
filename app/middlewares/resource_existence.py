from typing import Annotated, TypeVar

from fastapi import Request, HTTPException, Depends
from app.models import Course, Module, Lesson, db

T = TypeVar('T', type[Course], type[Module], type[Lesson])

class ResourceExistenceMiddleware:
    def __init__(self, resource_class: T, resource_id_path_parameter_name: str):
        self.resource_id_path_parameter_name = resource_id_path_parameter_name
        self.resource_class = resource_class

    def __call__(self, request: Request):
        resource_id = request.path_params.get(self.resource_id_path_parameter_name)
        if not resource_id:
            raise ValueError(f"Resource parameter name '{self.resource_id_path_parameter_name}' does not exist for current request.")

        try:
            resource_id = int(resource_id)
        except ValueError:
            ...

        with db.atomic():
            resource = self.resource_class.get_by_id(resource_id)
            if resource is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Resource '{self.resource_class.__name__}' with id {resource_id} was not found.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return resource


course_existence_middleware = ResourceExistenceMiddleware(Course, "course_id")
module_existence_middleware = ResourceExistenceMiddleware(Module, "module_id")
lesson_existence_middleware = ResourceExistenceMiddleware(Lesson, "lesson_id")

ExistentCourse = Annotated[Course, Depends(course_existence_middleware)]
ExistentLesson = Annotated[Lesson, Depends(lesson_existence_middleware)]
ExistentModule = Annotated[Module, Depends(module_existence_middleware)]
