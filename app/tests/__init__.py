from fastapi.testclient import TestClient

from app import app
from app.models import db, Course, User
from app.schemas.course import CourseForm
from app.schemas.lesson import LessonNestedForm
from app.schemas.module import ModuleNestedForm
from app.schemas.user import UserForm
from app.services.course import CourseService
from app.services.user import UserService

client = TestClient(app)

example_test_data = {
    'user': UserForm(name='name', password='password', email='test-email@email.com', cpf='73990286056'),

    'course': CourseForm(
        title="Introdução à computação gráfica com Blender I",
        modules=[
            ModuleNestedForm(
                title="Visão geral",
                lessons=[
                    LessonNestedForm(title="Introdução ao uso do Blender", video_link="EA3WYhPgCCM"),
                    LessonNestedForm(title="Instalação do Blender (Windows, Ubuntu e MacOs)", video_link="Ztcm1iWoWxM"),
                    LessonNestedForm(title="Visão geral da interface gráfica", video_link="2GJe_iIhD8E"),
                ]
            ),
            ModuleNestedForm(
                title="Usos da interface",
                lessons=[
                    LessonNestedForm(title="Uso em jogos", video_link="w0LAS3tuYBs"),
                    LessonNestedForm(title="Uso na indústria automobilística", video_link="WVNRCGriaGI"),
                    LessonNestedForm(title="Usos da medicina 3D e da biotecnologia", video_link="u6owJ0Wst8Q"),
                    LessonNestedForm(title="Uso nos mecanismos de acessibilidade para pessoas com deficiência visual", video_link="u6owJ0Wst8Q"),
                ]
            ),
        ]
    )
}

NUMBER_OF_LESSONS_IN_EXAMPLE_DATA = 7


def reset_database():
    with db.atomic():
        (
            Course
            .delete()
            .where(Course.title == example_test_data['course'].title)
        ).execute()

        (
            User
            .delete()
            .where(User.email == example_test_data['user'].email)
        ).execute()


def create_example_data():
    try:
        with db.atomic():
            user = UserService.register(example_test_data['user'])
            CourseService.register(example_test_data['course'], user)
    except:
        print("Não foi possível criar os dados")
