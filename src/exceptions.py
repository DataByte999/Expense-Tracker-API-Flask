from flask import jsonify, request
from psycopg import errors
from pydantic import ValidationError

# Custom App Errors
class AppError(Exception):
    """Base class for all custom app errors."""


class BadRequestError(AppError):
    pass


class UnauthorizedError(AppError):
    pass


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class BusinessRuleError(AppError):
    pass


class UnsupportedMediaTypeError(AppError):
    pass



# Global Error Handlers
def register_error_handlers(app):
    # Domain errors
    @app.errorhandler(BadRequestError)
    def handle_bad_request(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(e):
        return jsonify({"error": str(e)}), 401

    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(ConflictError)
    def handle_conflict(e):
        return jsonify({"error": str(e)}), 409

    @app.errorhandler(BusinessRuleError)
    def handle_business_rule(e):
        return jsonify({"error": str(e)}), 422

    @app.errorhandler(UnsupportedMediaTypeError)
    def handle_unsupported_media(e):
        return jsonify({"error": str(e)}), 415

    # Generic fallback
    @app.errorhandler(Exception)
    def handle_generic(e):
        app.logger.exception(f"Unhandled error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    # Pydantic validation errors
    @app.errorhandler(ValidationError)
    def handle_pydantic_error(e: ValidationError):
        return jsonify({"error": extract_loc_msg(e)}), 400

    # DB errors (psycopg)
    @app.errorhandler(errors.Error)
    def handle_db_error(e):
        app_error = translate_db_errors(e)
        return jsonify({"error": str(app_error)}), status_code_from_error(app_error)

    # Pre-request hook: enforce JSON payloads
    @app.before_request
    def ensure_json_payload():
        if request.method in ("POST", "PUT", "PATCH"):
            if not request.is_json:
                raise UnsupportedMediaTypeError("Content-Type must be application/json")
            if request.get_json(silent=True) is None:
                raise UnsupportedMediaTypeError("Request body must contain valid JSON")


# DB Error Translation
def translate_db_errors(e: Exception) -> AppError:
    """Translate psycopg errors into domain-level AppErrors."""

    # Common constraint violation
    if isinstance(e, errors.NotNullViolation):
        return BadRequestError("A required field is missing")

    if isinstance(e, errors.UniqueViolation):
        return ConflictError("Resource already exists")

    if isinstance(e, errors.CheckViolation):
        return BadRequestError("Constraint check failed")

    if isinstance(e, errors.ForeignKeyViolation):
        return NotFoundError("Related resource does not exist")

    # Type/format errors
    if isinstance(e, errors.InvalidTextRepresentation):
        return BadRequestError("Invalid input format")

    if isinstance(e, errors.InvalidDatetimeFormat):
        return BadRequestError("Invalid date format")

    # Catch all for ny unexpected Database error
    return AppError("Database error")


# Helper: Status codes from AppError
def status_code_from_error(e: AppError):
    if isinstance(e, BadRequestError):
        return 400
    if isinstance(e, UnauthorizedError):
        return 401
    if isinstance(e, NotFoundError):
        return 404
    if isinstance(e, ConflictError):
        return 409
    if isinstance(e, BusinessRuleError):
        return 422
    return 500


# Utility: Extract validation error details
def extract_loc_msg(e: ValidationError):
    """Return only 'loc' and 'msg' fields from Pydantic ValidationError."""
    return [{"loc": err["loc"], "msg": err["msg"]} for err in e.errors()]