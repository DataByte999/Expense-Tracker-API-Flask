from flask import jsonify
from psycopg import errors


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


def register_error_handlers(app):
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

    @app.errorhandler(Exception)
    def handle_generic(e):
        app.logger.exception(f"Unhandled error: {e}")
        return jsonify({"error": "Internal server error"}), 500


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