"""
URL configuration for starter_django_ninja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Schema
from core.models import Deck
from core.models import Card
from django.utils import timezone

api = NinjaAPI()


class HelloSchema(Schema):
    name: str = "world"


class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str


class Error(Schema):
    message: str


class DoesNotExist:
    pass


@api.post("/deck")
def create_deck(request, eyed: int):
    deck = Deck.objects.get(id=eyed)
    card_cat = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    card_val = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    for i in card_val:
        for j in card_cat:
            deck.card_set.create(suit=str(i), value=str(i) + " of " + str(j))
    print(deck.card_set.all())
    return {
            "created date": deck.creation_date,
            "id": deck.pk,
            "set": deck.card_set.count()
        }


@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user


@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"


@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
