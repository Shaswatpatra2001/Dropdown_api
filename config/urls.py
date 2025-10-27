from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema Configuration
schema_view = get_schema_view(
    
    openapi.Info(
        title="Odisha Location API",
        default_version='v1.0',
        description="""
        Comprehensive API for Indian location data including states, districts, blocks, and villages.
        
        **Features:**
        - 🌍 Get all 36 Indian states/UTs
        - 🏛️ Get districts for any state  
        - 🏘️ Get blocks/sub-districts for any district
        - 🏡 Get villages for any block
        
        **Smart Parameter Detection:** The API automatically determines what data to return based on the parameters you provide.
        
        
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@company.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('location_app.urls')),
    
    # API Documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]