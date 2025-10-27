from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import location_service

# Define response schemas for Swagger
success_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        'data': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING),
            example=['Item1', 'Item2', 'Item3']
        ),
        'filters': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'state': openapi.Schema(type=openapi.TYPE_STRING, example='odisha'),
                'district': openapi.Schema(type=openapi.TYPE_STRING, example='khordha'),
                'block': openapi.Schema(type=openapi.TYPE_STRING, example='jankia'),
            }
        ),
        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Data fetched successfully'),
        'metadata': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, example=3),
                'filters_applied': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    example=['state', 'district']
                )
            }
        )
    }
)

error_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        'error': openapi.Schema(type=openapi.TYPE_STRING, example='Missing required parameters'),
        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Please provide state parameter'),
        'filters': openapi.Schema(type=openapi.TYPE_OBJECT, example={})
    }
)

class LocationAPIView(APIView):
    """
    Single API for All Location Data - States, Districts, Blocks, and Villages
    """
    
    @swagger_auto_schema(
        operation_summary="Get hierarchical location data",
        operation_description="""
        Smart API that returns location data based on parameters provided:
        
        - **No parameters**: Returns all states
        - **Only state**: Returns districts in that state
        - **State + district**: Returns blocks in that district  
        - **State + district + block**: Returns villages in that block
        
        You can also use the 'type' parameter to explicitly specify what data to return.
        """,
        manual_parameters=[
            openapi.Parameter(
                'state',
                openapi.IN_QUERY,
                description="State name (e.g., 'odisha', 'karnataka')",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'district', 
                openapi.IN_QUERY,
                description="District name (e.g., 'khordha', 'puri')",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'block',
                openapi.IN_QUERY, 
                description="Block/Sub-district name (e.g., 'jankia', 'puri sadar')",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'type',
                openapi.IN_QUERY,
                description="Explicitly specify data type to return",
                type=openapi.TYPE_STRING,
                enum=['states', 'districts', 'blocks', 'villages'],
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully fetched location data",
                schema=success_response_schema,
                examples={
                    "application/json": {
                        "states_example": {
                            "value": {
                                "success": True,
                                "data": ["Odisha", "Karnataka", "Tamil Nadu"],
                                "filters": {},
                                "message": "Found 36 states",
                                "metadata": {
                                    "total_count": 36,
                                    "filters_applied": []
                                }
                            }
                        },
                        "districts_example": {
                            "value": {
                                "success": True,
                                "data": ["Khordha", "Puri", "Cuttack"],
                                "filters": {"state": "odisha"},
                                "message": "Found 30 districts in odisha", 
                                "metadata": {
                                    "total_count": 30,
                                    "filters_applied": ["state"]
                                }
                            }
                        },
                        "blocks_example": {
                            "value": {
                                "success": True,
                                "data": ["Jankia", "Balipatna", "Jatni"],
                                "filters": {"state": "odisha", "district": "khordha"},
                                "message": "Found 15 blocks in khordha, odisha",
                                "metadata": {
                                    "total_count": 15,
                                    "filters_applied": ["state", "district"]
                                }
                            }
                        },
                        "villages_example": {
                            "value": {
                                "success": True,
                                "data": ["Badagotha", "Badasankula", "Balipatna"],
                                "filters": {"state": "odisha", "district": "khordha", "block": "jankia"},
                                "message": "Found 120 villages in jankia, khordha, odisha",
                                "metadata": {
                                    "total_count": 120,
                                    "filters_applied": ["state", "district", "block"]
                                }
                            }
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request - missing or invalid parameters",
                schema=error_response_schema,
                examples={
                    "application/json": {
                        "missing_state": {
                            "value": {
                                "success": False,
                                "error": "State parameter is required for districts",
                                "message": "Please provide state parameter",
                                "filters": {}
                            }
                        },
                        "missing_district": {
                            "value": {
                                "success": False,
                                "error": "Both state and district parameters are required for blocks", 
                                "message": "Please provide state and district parameters",
                                "filters": {"state": "odisha"}
                            }
                        }
                    }
                }
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=error_response_schema,
                examples={
                    "application/json": {
                        "server_error": {
                            "value": {
                                "success": False,
                                "error": "Error connecting to database",
                                "message": "Error fetching location data", 
                                "filters": {"state": "odisha"}
                            }
                        }
                    }
                }
            )
        },
        tags=['Locations']
    )
    def get(self, request):
        """
        Get hierarchical location data
        
        Examples:
        - GET /api/locations/ → All states
        - GET /api/locations/?state=odisha → Districts in Odisha
        - GET /api/locations/?state=odisha&district=khordha → Blocks in Khordha
        - GET /api/locations/?state=odisha&district=khordha&block=jankia → Villages in Jankia
        """
        
        state = request.GET.get('state', '').strip()
        district = request.GET.get('district', '').strip()
        block = request.GET.get('block', '').strip()
        data_type = request.GET.get('type', '').strip().lower()
        
        filters = {}
        if state:
            filters['state'] = state
        if district:
            filters['district'] = district
        if block:
            filters['block'] = block
        
        try:
            # If specific type is requested
            if data_type:
                if data_type == 'states':
                    data = location_service.get_states()
                    message = f"Found {len(data)} states"
                
                elif data_type == 'districts':
                    if not state:
                        return Response({
                            'success': False,
                            'error': 'State parameter is required for districts',
                            'message': 'Please provide state parameter'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    data = location_service.get_districts(state)
                    message = f"Found {len(data)} districts in {state}"
                
                elif data_type == 'blocks':
                    if not state or not district:
                        return Response({
                            'success': False,
                            'error': 'Both state and district parameters are required for blocks',
                            'message': 'Please provide state and district parameters'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    data = location_service.get_blocks(state, district)
                    message = f"Found {len(data)} blocks in {district}, {state}"
                
                elif data_type == 'villages':
                    if not all([state, district, block]):
                        return Response({
                            'success': False,
                            'error': 'State, district and block parameters are required for villages',
                            'message': 'Please provide state, district and block parameters'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    data = location_service.get_villages(state, district, block)
                    message = f"Found {len(data)} villages in {block}, {district}, {state}"
                
                else:
                    return Response({
                        'success': False,
                        'error': 'Invalid type parameter',
                        'message': 'Type must be: states, districts, blocks, or villages'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Auto-detect based on parameters
            else:
                if not state and not district and not block:
                    data = location_service.get_states()
                    message = f"Found {len(data)} states"
                
                elif state and not district and not block:
                    data = location_service.get_districts(state)
                    message = f"Found {len(data)} districts in {state}"
                
                elif state and district and not block:
                    data = location_service.get_blocks(state, district)
                    message = f"Found {len(data)} blocks in {district}, {state}"
                
                elif state and district and block:
                    data = location_service.get_villages(state, district, block)
                    message = f"Found {len(data)} villages in {block}, {district}, {state}"
                
                else:
                    return Response({
                        'success': False,
                        'error': 'Invalid parameter combination',
                        'message': 'Parameters must be provided in hierarchical order: state → district → block'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': True,
                'data': data,
                'filters': filters,
                'message': message,
                'metadata': {
                    'total_count': len(data),
                    'filters_applied': list(filters.keys())
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error fetching location data',
                'filters': filters
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)