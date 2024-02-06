from django.urls import reverse
from django.test import RequestFactory
from DB.models import Users

from User_create.views import UserCreate

import pytest
#-------------------------------------------------------------------#

@pytest.mark.django_db
def test_user():

#1 - Creamos una instancia de la vista
    view = UserCreate.as_view()

#2 - Creamos los datos de un usuario de prueba
    user_data = {
        'username':'leonfio',
        'first_name':'Leonardo',
        'last_name':'Fiorentino',
        'email':'leonfio1515@gmail.com',
        'password':'Cybe1234',
    }

#3 - Creamos el objeto de un usuario de prueba
    Users.objects.create_user(**user_data)

#4 - Creamos una solicitud falsa para la vista
    factory = RequestFactory()
    request = factory.post(reverse('register'), data=user_data)
    request.user = Users.objects.get(username = 'leonfio')

#5 - Llamamos a la vista
    response = view(request)

#6 - Verificamos la respuesta y la creacion del usuario.
    assert response.status_code == 302
    assert Users.objects.filter(username = 'leonfio').exists()