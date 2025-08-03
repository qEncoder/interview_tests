"""Integration tests for the Scopes API.

These tests cover the POST /api/v1/scopes endpoint and make sure that
1. A scope can be created successfully.
2. Payload validation errors are surfaced correctly.
3. Attempting to create a scope with a duplicate UUID is rejected.
"""

from __future__ import annotations

import uuid
from httpx import AsyncClient

import pytest

SCOPES_ENDPOINT = "/api/v1/scopes"


@pytest.mark.asyncio
async def test_create_scope_success(async_client: AsyncClient) -> None:
    """A valid payload should create a new scope and return HTTP 201."""

    payload = {
        "name": "test_scope",
        "uuid": str(uuid.uuid4()),
    }

    response = await async_client.post(SCOPES_ENDPOINT, json=payload)

    assert response.status_code == 201
    # The API echoes the created object back to the caller.
    assert response.json() == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        # Name is too short (min_length=3)
        {"name": "aa", "uuid": str(uuid.uuid4())},
        # UUID is not a valid RFC-4122 UUID string
        {"name": "test_scope", "uuid": "not-a-uuid"},
    ],
)
async def test_create_scope_validation_error(async_client: AsyncClient, payload: dict) -> None:
    """Invalid payloads should be rejected with a 422 status code."""
    response = await async_client.post(SCOPES_ENDPOINT, json=payload)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_scope_duplicate_uuid(async_client: AsyncClient) -> None:
    """Creating two scopes with the same UUID should fail with HTTP 400 on the second call."""

    duplicate_uuid = str(uuid.uuid4())

    first_payload = {"name": "first_scope", "uuid": duplicate_uuid}
    second_payload = {"name": "second_scope", "uuid": duplicate_uuid}

    # First creation succeeds.
    first_response = await async_client.post(SCOPES_ENDPOINT, json=first_payload)
    assert first_response.status_code == 201

    # Second creation with the same UUID should fail.
    second_response = await async_client.post(SCOPES_ENDPOINT, json=second_payload)
    assert second_response.status_code == 400
    assert "already in use" in second_response.json().get("detail", "")
