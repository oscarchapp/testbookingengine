from django.test import TestCase

# Create your tests here.

#By Nauzet
class MyTestCase1(TestCase):

    # Only use setUp() and tearDown() if necessary

    def date(self):
        response = self.client.post(str(self.booking.pk)+'/date/edit', data={ 'start_date': '2020-01-01', 'end_date': '2020-01-02' })
        self.assertEqual(response.status_code, 404)

    def Edit_booking(self):
        response = self.client.post('/booking/'+str(self.booking.pk)+'/edit', data={ 'start_date': '2020-01-01', 'end_date': '2020-01-02' })
        self.assertEqual(response.status_code, 302)

    
        # Test feature two.
   

# class MyTestCase2(unittest.TestCase):
#     ... same structure as MyTestCase1 ...

# ... more test classes ...

# if __name__ == '__main__':
#     unittest.main()