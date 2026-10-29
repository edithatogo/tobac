"""Fail closed on the declared MOH rehearsal inventory before native restore.

This validates only the nine-object exploratory bundle against an inventory already
verified by the native store. It does not establish source registration, historical
capture time, provenance graph closure, or independent preservation.
"""

from __future__ import annotations

from typing import Any, cast

OBJECT_COUNT = 9
SHA_LENGTH = 64


def _list(value: object) -> list[Any]:
    if not isinstance(value, list):
        msg = "Rehearsal inventory or records are missing"
        raise TypeError(msg)
    return cast("list[Any]", value)


def _object(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        msg = "Rehearsal object entry is invalid"
        raise TypeError(msg)
    return cast("dict[str, Any]", value)


def _native_objects(objects: list[Any], expected: set[str]) -> dict[str, int]:
    actual: dict[str, int] = {}
    for item in objects:
        obj = _object(item)
        oid, size = obj.get("object_id"), obj.get("byte_count")
        if not isinstance(oid, str) or type(size) is not int or size < 0 or oid in actual:
            msg = "Rehearsal native object is invalid or duplicated"
            raise ValueError(msg)
        actual[oid] = size
    if set(actual) != expected:
        msg = "Rehearsal native inventory differs from expected identities"
        raise ValueError(msg)
    return actual


def _records(records: list[Any], expected: set[str], actual: dict[str, int]) -> None:
    seen: set[str] = set()
    for item in records:
        record = _object(item)
        oid, sha, size = record.get("record_id"), record.get("sha256"), record.get("size_bytes")
        if (
            not isinstance(oid, str)
            or not isinstance(sha, str)
            or oid != "sha256:" + sha
            or type(size) is not int
            or oid in seen
            or actual.get(oid) != size
        ):
            msg = "Rehearsal record is invalid, duplicated, or mismatched"
            raise ValueError(msg)
        seen.add(oid)
    if seen != expected:
        msg = "Rehearsal records do not cover declared objects"
        raise ValueError(msg)


def check_rehearsal_manifest(
    manifest: dict[str, Any], inventory: dict[str, Any], expected_ids: list[str]
) -> None:
    """Compare native-verified object identities, sizes, count, and inventory root."""
    objects = _list(inventory.get("objects"))
    records = _list(manifest.get("records"))
    if len(expected_ids) != OBJECT_COUNT or len(set(expected_ids)) != OBJECT_COUNT:
        msg = "Rehearsal must declare nine unique expected objects"
        raise ValueError(msg)
    if (
        len(objects) != OBJECT_COUNT
        or len(records) != OBJECT_COUNT
        or manifest.get("records_count") != OBJECT_COUNT
    ):
        msg = "Rehearsal must contain exactly nine objects and records"
        raise ValueError(msg)
    root = inventory.get("inventory_sha256")
    if not isinstance(root, str) or len(root) != SHA_LENGTH or manifest.get("sha256_root") != root:
        msg = "Rehearsal inventory root differs"
        raise ValueError(msg)
    expected = set(expected_ids)
    _records(records, expected, _native_objects(objects, expected))
