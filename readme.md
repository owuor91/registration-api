# Courses Service

Courses service is a REST API for registering students to courses. 

Supported functionality:
- Register a student
- Login a student
- Create a course
- List existing courses
- Register student to existing course
- Get student's enrolled courses

## Usage
### Register a student
`POST https://courses-service.herokuapp.com/register`

EXAMPLE:
```
http --form POST https://courses-service.herokuapp.com/register first_name="Cate" last_name="Ajab" phone_number="0700000001" email="cate@ajab.com" password="cate_ajab"
```

Response:
```
{
    "message": "student registration, successful",
    "student": {
        "date_of_birth": "2000-05-16 00:00:00",
        "email": "cate@ajab.com",
        "first_name": "Cate",
        "image_url": "",
        "last_name": "Ajab",
        "phone_number": "0700000001",
        "student_id": "b8da807a-5117-4278-b993-def96e62e2ca"
    }
}
```

### Login a Student
`POST https://courses-service.herokuapp.com/login`

EXAMPLE:
```
http --form POST https://courses-service.herokuapp.com/login email="cate@ajab.com" password="cate_ajab"
```
Response:
```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTczMjYzNDAsIm5iZiI6MTU5NzMyNjM0MCwianRpIjoiNjlhODU2MmYtM2E0OC00ODU1LTkwMTUtNjM4MTI2NDg5NDBkIiwiZXhwIjoxNTk3NDEyNzQwLCJpZGVudGl0eSI6ImI4ZGE4MDdhLTUxMTctNDI3OC1iOTkzLWRlZjk2ZTYyZTJjYSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.YkxstC33kqlhzn57UqCAZHU8f0wcFVMHjgYNrHI6qLc",
    "message": "login successful",
    "student_id": "b8da807a-5117-4278-b993-def96e62e2ca"
}
```

### Create a course
`POST https://courses-service.herokuapp.com/courses`

EXAMPLE:
```
http --form POST https://courses-service.herokuapp.com/courses course_name="Android App Development" course_code="AAD 101" instructor="John Owuor" description="Learn how to build android apps" "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTczMjYzNDAsIm5iZiI6MTU5NzMyNjM0MCwianRpIjoiNjlhODU2MmYtM2E0OC00ODU1LTkwMTUtNjM4MTI2NDg5NDBkIiwiZXhwIjoxNTk3NDEyNzQwLCJpZGVudGl0eSI6ImI4ZGE4MDdhLTUxMTctNDI3OC1iOTkzLWRlZjk2ZTYyZTJjYSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.YkxstC33kqlhzn57UqCAZHU8f0wcFVMHjgYNrHI6qLc"
```
Response:
```
{
    "course": {
        "course_code": "AAD 101",
        "course_id": "37f2cbcb-e4c4-4cef-9bce-ff4ff67a3678",
        "course_name": "Android App Development",
        "description": "Learn how to build android apps",
        "instructor": "John Owuor"
    },
    "message": "course added successfully"
}
```

### List existing courses
`GET https://courses-service.herokuapp.com/courses`

EXAMPLE:
```
http GET https://courses-service.herokuapp.com/courses  "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTczMjYzNDAsIm5iZiI6MTU5NzMyNjM0MCwianRpIjoiNjlhODU2MmYtM2E0OC00ODU1LTkwMTUtNjM4MTI2NDg5NDBkIiwiZXhwIjoxNTk3NDEyNzQwLCJpZGVudGl0eSI6ImI4ZGE4MDdhLTUxMTctNDI3OC1iOTkzLWRlZjk2ZTYyZTJjYSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.YkxstC33kqlhzn57UqCAZHU8f0wcFVMHjgYNrHI6qLc"
```
Response:
```
{
    "courses": [
        {
            "course_code": "DBA 101",
            "course_id": "36b25f24-77b5-4781-94b2-73e8bf6d0008",
            "course_name": "Database Administration",
            "description": "Introduction to DBA with PSQL",
            "instructor": "Jane Hewi"
        },
        {
            "course_code": "WBD 101",
            "course_id": "73cb3988-93b9-46f4-b149-a93a33b44ca3",
            "course_name": "HTML",
            "description": "HTML CSS & JS for websites",
            "instructor": "Matt Kato"
        },
        {
            "course_code": "AAD 101",
            "course_id": "37f2cbcb-e4c4-4cef-9bce-ff4ff67a3678",
            "course_name": "Android App Development",
            "description": "Learn how to build android apps",
            "instructor": "John Owuor"
        }
    ]
}
```

### Register student to existing course
`POST https://courses-service.herokuapp.com/register-course`

EXAMPLE:
```
http --form POST https://courses-service.herokuapp.com/register-course student_id="b8da807a-5117-4278-b993-def96e62e2ca" course_id="37f2cbcb-e4c4-4cef-9bce-ff4ff67a3678"  "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTczMjYzNDAsIm5iZiI6MTU5NzMyNjM0MCwianRpIjoiNjlhODU2MmYtM2E0OC00ODU1LTkwMTUtNjM4MTI2NDg5NDBkIiwiZXhwIjoxNTk3NDEyNzQwLCJpZGVudGl0eSI6ImI4ZGE4MDdhLTUxMTctNDI3OC1iOTkzLWRlZjk2ZTYyZTJjYSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.YkxstC33kqlhzn57UqCAZHU8f0wcFVMHjgYNrHI6qLc"
```
Response:
```
{
    "message": "success",
    "registration": {
        "course_id": "37f2cbcb-e4c4-4cef-9bce-ff4ff67a3678",
        "student_id": "b8da807a-5117-4278-b993-def96e62e2ca"
    }
}
```

### Get student's enrolled courses
`GET https://courses-service.herokuapp.com/students/{student_id}/courses`

EXAMPLE:
```
http GET https://courses-service.herokuapp.com/students/b8da807a-5117-4278-b993-def96e62e2ca/courses  "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTczMjYzNDAsIm5iZiI6MTU5NzMyNjM0MCwianRpIjoiNjlhODU2MmYtM2E0OC00ODU1LTkwMTUtNjM4MTI2NDg5NDBkIiwiZXhwIjoxNTk3NDEyNzQwLCJpZGVudGl0eSI6ImI4ZGE4MDdhLTUxMTctNDI3OC1iOTkzLWRlZjk2ZTYyZTJjYSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.YkxstC33kqlhzn57UqCAZHU8f0wcFVMHjgYNrHI6qLc"
```
Response:
```
{
    "student_courses": [
        {
            "course_code": "AAD 101",
            "course_id": "37f2cbcb-e4c4-4cef-9bce-ff4ff67a3678",
            "course_name": "Android App Development",
            "description": "Learn how to build android apps",
            "instructor": "John Owuor"
        }
    ]
}
```