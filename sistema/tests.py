# from rest_framework.test import APITestCase, APIClient

# class CursosTestCase(APITestCase):
#     client = APIClient()
#     def test_post(self):
#         request= self.client.post('/sistema/cursos/')
#         print(request)
#         print(request.status_code)
#         print(request.data)
#         message = request.data.get('message')
#         self.assertEqual(request.status_code,400)
#         self.assertEqual(message,'Error al crear el curso')