# GeoAuth Plugin Documentation

## 📌 Overview
GeoAuth is a Django plugin that provides authentication and user-related utilities with geo-location support. It allows users to:

1. Get website visitors' IP addresses.
2. Retrieve device and browser details.
3. Access location data, including country, language, and more.
4. Restrict user registration based on allowed countries.

The plugin includes middleware, utility functions, and API endpoints to facilitate easy integration.

---

## 📥 Installation & Setup

1. Install the package:

```bash
pip install geo-auth
```

2. Add `geo_auth` to your Django `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'geo_auth',
]
```

3. Add the middleware to your `MIDDLEWARE` settings:

```python
MIDDLEWARE = [
    ...
    'geo_auth.middleware.GeoAuthMiddleware',
]
```

4. Run migrations:

```bash
python manage.py migrate geo_auth
```

---

## 🚀 Features & Usage

### 1️⃣ **Middleware**
The middleware automatically captures visitor IP and device details.
To use it, just add it to `MIDDLEWARE` in `settings.py` (already shown above).

### 2️⃣ **Utility Functions**
You can call utility functions directly in your views:

```python
from geo_auth.utils import get_user_ip, get_device_info, get_location_data

def my_view(request):
    user_ip = get_user_ip(request)
    device_info = get_device_info(request)
    location_data = get_location_data(request)
    return JsonResponse({"ip": user_ip, "device": device_info, "location": location_data})
```

### 3️⃣ **API Endpoints**
The plugin provides built-in API views:

| Endpoint               | Method | Description                         |
|------------------------|--------|-------------------------------------|
| `/geo/ip/`             | GET    | Get visitor's IP address.          |
| `/geo/device/`         | GET    | Get device/browser details.        |
| `/geo/location/`       | GET    | Get user location details.         |
| `/auth/register/`      | POST   | Register a new user.               |
| `/auth/login/`         | POST   | User login.                        |

Example request:

```bash
curl -X GET http://127.0.0.1:8000/geo/ip/
```

---

## 🛠 Customizing the User Registration Serializer

Users can **override** the `UserRegistrationSerializer` to add custom fields, validation, or saving logic.

### ✅ **How to Extend the Serializer**

```python
from geo_auth.serializers import UserRegistrationSerializer

class CustomUserRegistrationSerializer(UserRegistrationSerializer):
    phone_number = serializers.CharField(max_length=15, required=True)

    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + ["phone_number"]
```

### ✅ **Overriding the Save Method**
Users can modify how data is saved into the `User` model:

```python
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserRegistrationSerializer(UserRegistrationSerializer):
    phone_number = serializers.CharField(max_length=15, required=True)

    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + ["phone_number"]

    def create(self, validated_data):
        phone_number = validated_data.pop("phone_number")
        user = super().create(validated_data)
        user.phone_number = phone_number
        user.save()
        return user
```

### ✅ **Adding Custom Password Validation**

```python
class CustomUserRegistrationSerializer(UserRegistrationSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + ["confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # Remove before saving
        return super().create(validated_data)
```

---

## 🔗 **Using the Custom Serializer in a View**

After overriding the serializer, users can use it in their views:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserRegistrationSerializer

class CustomRegisterView(APIView):
    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

## 🎯 **Conclusion**
- The plugin provides **ready-to-use authentication & geo-tracking features**.
- Users can **override the serializer** to customize validation and user saving logic.
- Middleware, utility functions, and API endpoints make integration easy.
- The system is **flexible** and **extensible** for different project needs.

🚀 **Now users can integrate and customize GeoAuth as needed!**

