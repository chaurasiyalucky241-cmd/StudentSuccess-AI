from .student_routes import router as student_router
from .analytics_routes import router as analytics_router
from .prediction_routes import router as predictions_router
from .auth_routes import router as auth_router

__all__ = ["student_router", "analytics_router", "predictions_router", "auth_router"]
