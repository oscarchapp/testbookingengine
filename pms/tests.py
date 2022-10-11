from django.test import TestCase, Client
from .models import Room, Booking, Customer
from datetime import datetime, timedelta
from django.utils import timezone

# Create your tests here.
class TestViews(TestCase):
    def setUp(self):
        # La funcion setUp se ejecuta antes de cada Test
        
        # Inicializamos el cliente
        self.client = Client(HTTP_USER_AGENT='Mozilla/6.0')

        # Creamos datos de prueba para los tests
        # Customer 
        Customer.objects.create(name="Test", email="test@test.es", phone="123456789").save()

        # Habitaciones
        Room.objects.create(name="Room 1.1", description="Simple test").save()
        Room.objects.create(name="Room 2.1", description="Double test").save()

        # Reservas
        Booking.objects.create(state="NEW",
            checkin =  datetime.now(),
            checkout = datetime.now() + timedelta(days=1),
            room = Room.objects.get(name="Room 1.1"),
            guests = 1,
            customer = Customer.objects.get(name="Test"),
            total = 100.0 ,
            code = 'AB123456',
            created = datetime.now(),        
        ).save()
        
        # PRINTS PARA DEBUG TESTS
        # print('response.content: ' , response.content) # Devuelve todo el contenido
        # print('response.request: ' , response.request) # Devuelve los datos de la peticion
        # print('response.items: ' , response.items()) # Devuelve los datos de la respuesta
        # print('response.status_code: ' , response.status_code) # Devuelve el estado de la respuesta

        print('- '*32 , "\n")

    def test_RoomSearch(self):
        # Comprueba que funcione la búsqueda de habitaciones        

        # Peticion POST con los datos del formulario
        response = self.client.post('/rooms/', {'btn_search_room':'Room 1', 'form_name':'search_room'})
 
        # Comrpobamos que haya resultados de Room 1
        self.assertContains(response, '<div class="">\n      Room 1.1 (None)\n    </div>') 

        # Comprobamos que no haya resultados de Room 2
        self.assertNotContains(response, '<div class="">\n      Room 2.1 (None)\n    </div>') 

    def test_AvailabityWidget(self):
        # Comprueba que funcione el widget de disponibilidad        

        # Petición GET para cargar el HTML de los widgets
        response = self.client.get('/dashboard/')

        # Comrobamos que el widget de % ocupacion no este a 0.0
        
        self.assertContains(response, '<h5 class="small">% Ocupación</h5>\n      <h1 class="dashboard-value">0.5%</h1>')

    def test_ChangeBookingDateOK(self):
        # Comprueba el cambio de fechas de una reserva con éxito

        # Sacamos la reserva de prueba
        booking = Booking.objects.get(code="AB123456")
        
        # Peticion POST con los datos del formulario
        response = self.client.post('/booking/{0}/edit_dates'.format(booking.id), {'booking-checkin':'2022-10-10', 'booking-checkout':'2022-10-13'}, secure=True)

        # Revisamos si el mensaje es el de cambio con éxito
        self.assertContains(response, '<span class="border border-success text-success w-auto p4 fs-4 mb-4">Fechas de la reserva cambiadas correctamente</span>')
        
    def test_ChangeBookingDateNOK(self):
        # Comprueba el cambio de fechas de una reserva con éxito

        # Sacamos la reserva de prueba
        booking = Booking.objects.get(code="AB123456")

        checkin =  datetime.now()
        checkout = datetime.now() + timedelta(days=1)     

        # Peticion POST con los datos del formulario
        response = self.client.post('/booking/{0}/edit_dates'.format(booking.id), {'booking-checkin':'{0}'.format(checkin.strftime('%Y-%m-%d')), 'booking-checkout':'{0}'.format(checkout.strftime('%Y-%m-%d'))}, secure=True)

        # Revisamos si el mensaje es el de cambio con éxito
        self.assertContains(response, '<span class="border border-danger text-danger w-auto p4 fs-4 mb-4">No hay disponibilidad para las fechas seleccionadas</span>')
        