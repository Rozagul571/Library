Library Management API
Bu Django REST Framework (DRF) yordamida yaratilgan kutubxona tizimi uchun REST API. SQLite database ishlatilgan. Tizimda foydalanuvchilarni boshqarish, kitoblar band qilish va baho berish imkoniyatlari mavjud.
Default Users (Standart Foydalanuvchilar)
Birinchi marta kirganingizda quyidagi foydalanuvchilar avtomatik yaratiladi:

Authentication (Kirish)

Admin: \

username: rozagul
password: 1234
role: admin


Operator: 
username: operator
password: operator1
role: operator


User: 
username: Nodirbekova
password: Nodirbekova
role: user





Birinchi Tekshiruvchi Uchun Qanday Qilish Kerak?
Agar siz bu tizimni birinchi marta tekshirayotgan bo‘lsangiz, quyidagi qadamlarni osonlikcha bajaring:
1. Tizimni Yuklab Olish

Loyihani kompyuteringizga yuklang. Agar GitHub’dan olgan bo‘lsangiz:
Terminal oching va quyidagi buyruqlarni yozing:git clone <loyihaning-url-si>
cd library-api





2. Docker’ni O‘rnatish

Kompyuteringizda Docker va Docker Compose o‘rnatilgan bo‘lishi kerak. Agar yo‘q bo‘lsa:
Internetdan "Docker Desktop" ni yuklab oling va o‘rnating.
O‘rnatgandan keyin Docker ishlayotganiga ishonch hosil qiling.



3. Tizimni Ishga Tushirish

Terminalda loyiha papkasida bo‘lsangiz (masalan, library-api papkasi ichida), quyidagi buyruqni yozing:docker-compose up --build


Bir oz kuting (birinchi marta 2-3 daqiqa). Tizim ishga tushgandan keyin brauzerda http://127.0.0.1:8080/ manziliga o‘ting va API hujjatlarini ko‘ring.

4. Tizimga Kirish va Sinash

Tizim ishga tushgandan so‘ng, quyidagi foydalanuvchilardan biri bilan kirishni sinab ko‘ring:

Admin (rozagul) bilan sinash:
Postman yoki terminalda yangi so‘rov yarating:
Method: POST
URL: http://127.0.0.1:8080/api/v1/token/
Body (JSON formatida):
{
  "username": "rozagul",
  "password": "1234"
}




"Send" tugmasini bosing yoki curl bilan:curl -X POST 'http://127.0.0.1:8080/api/v1/token/' -H 'Content-Type: application/json' -d '{"username": "rozagul", "password": "1234"}'


Javobda access token olasiz, masalan:{
  "refresh": "<uzun-string>",
  "access": "<sizning-tokeningiz>",
  "role": "admin"
}


Bu token’ni keyingi so‘rovlarda Authorization: Bearer <token> sifatida ishlatasiz.




Operator (operator) yoki User (Nodirbekova) bilan ham xuddi shu tarzda sinab ko‘ring, faqat username va parolni o‘zgartiring.


5. Asosiy Amallarni Tekshirish

Admin sifatida:

Yangi kitob qo‘shishni sinab ko‘ring:
URL: http://127.0.0.1:8080/api/v1/books/create/
Method: POST
Body:{
  "title": "Yangi Kitob",
  "daily_price": 1500
}


Token bilan yuboring.


Foydalanuvchi qo‘shishni sinab ko‘ring:
URL: http://127.0.0.1:8080/api/v1/users/create/
Body:{
  "username": "yangiuser",
  "password": "parol123",
  "role": "user"
}






Operator sifatida:

Kitob ro‘yxatini ko‘rish:
URL: http://127.0.0.1:8080/api/v1/books/
Method: GET


Buyurtma qabul qilish:
URL: http://127.0.0.1:8080/api/v1/orders/1/take/
Method: POST
Token bilan yuboring.




User sifatida:

Kitob band qilish:
URL: http://127.0.0.1:8080/api/v1/orders/create/
Method: POST
Body:{
  "book": 1
}


Token bilan yuboring.


Baho berish:
URL: http://127.0.0.1:8080/api/v1/ratings/create/
Method: POST
Body:{
  "book": 1,
  "score": 4
}


Token bilan yuboring.






