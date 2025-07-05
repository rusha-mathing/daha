#!/usr/bin/env python3
"""
Test script to verify backend improvements are working correctly.
"""
import pytest
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.asyncio
async def test_imports():
    """Test that all new modules can be imported correctly."""
    print("🔍 Testing imports...")

    try:
        # Test core modules
        from app.core.exceptions import DatabaseError, NotFoundError, ValidationError, ConflictError
        print("✅ Custom exceptions imported successfully")

        from app.core.services import BaseService, CourseService, subject_service, course_service
        print("✅ Service layer imported successfully")

        from app.core.middleware import LoggingMiddleware, ErrorHandlingMiddleware
        print("✅ Middleware imported successfully")

        from app.core.models import (
            PaginationParams, PaginatedResponse, CourseFilters,
            SubjectResponse, CourseResponse
        )
        print("✅ Enhanced models imported successfully")

        from app.core.config import settings
        print("✅ Configuration imported successfully")

        from app.core.improved_router import improved_router
        print("✅ Improved router imported successfully")

        from app.api import create_app
        print("✅ Main API imported successfully")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


@pytest.mark.asyncio
async def test_configuration():
    """Test configuration settings."""
    print("\n🔧 Testing configuration...")

    try:
        from app.core.config import settings

        # Test basic settings
        assert settings.database_url is not None
        assert settings.api_title == "Daha Admin API"
        assert settings.debug is True
        assert len(settings.allowed_origins) > 0

        print("✅ Configuration settings are valid")
        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


@pytest.mark.asyncio
async def test_models():
    """Test enhanced models."""
    print("\n📋 Testing enhanced models...")

    try:
        from app.core.models import PaginationParams, CourseFilters, SubjectCreate

        # Test pagination params
        pagination = PaginationParams(page=1, size=10)
        assert pagination.page == 1
        assert pagination.size == 10

        # Test course filters
        filters = CourseFilters(subject="math", difficulty="beginner", search="algebra")
        assert filters.subject == "math"
        assert filters.difficulty == "beginner"
        assert filters.search == "algebra"

        # Test subject create
        subject = SubjectCreate(
            type="test",
            label="Test Subject",
            icon="test-icon",
            color="#000000",
            additional_description=["Test description"]
        )
        assert subject.type == "test"

        print("✅ Enhanced models are working correctly")
        return True

    except Exception as e:
        print(f"❌ Model error: {e}")
        return False


@pytest.mark.asyncio
async def test_exceptions():
    """Test custom exceptions."""
    print("\n⚠️ Testing custom exceptions...")

    try:
        from app.core.exceptions import DatabaseError, NotFoundError, ValidationError, ConflictError

        # Test exception creation
        db_error = DatabaseError("Test database error")
        assert db_error.status_code == 500
        assert "Test database error" in db_error.detail

        not_found = NotFoundError("Course", 123)
        assert not_found.status_code == 404
        assert "Course with id 123 not found" in not_found.detail

        validation_error = ValidationError("Test validation error")
        assert validation_error.status_code == 400

        conflict_error = ConflictError("Test conflict error")
        assert conflict_error.status_code == 409

        print("✅ Custom exceptions are working correctly")
        return True

    except Exception as e:
        print(f"❌ Exception error: {e}")
        return False


@pytest.mark.asyncio
async def test_app_creation():
    """Test that the FastAPI app can be created."""
    print("\n🚀 Testing app creation...")

    try:
        from app.api import create_app

        # Create the app
        app = create_app()

        # Check basic app properties
        assert app.title == "Daha Admin API"
        assert app.version == "1.0.0"
        assert app.debug is True

        # Check that routers are included
        assert len(app.routes) > 0

        print("✅ FastAPI app created successfully")
        return True

    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False


async def main():
    """Run all tests."""
    print("🧪 Testing Backend Improvements\n")
    print("=" * 50)

    tests = [
        test_imports,
        test_configuration,
        test_models,
        test_exceptions,
        test_app_creation,
    ]

    results = []
    for test in tests:
        result = await test()
        results.append(result)

    print("\n" + "=" * 50)
    print("📊 Test Results:")

    passed = sum(results)
    total = len(results)

    for i, result in enumerate(results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Test {i + 1}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Backend improvements are working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
