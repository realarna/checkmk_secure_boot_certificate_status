#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
)


@dataclass(frozen=True)
class SecureBootCertData:
    secureboot: str  # "True"/"False"/"Unsupported"/"Unknown"
    has_2011: int
    has_2023: int
    db_has_windows_uefi_ca_2023: int
    kek_has_kek_2k_2023: int


def _parse_kv(string_table: StringTable) -> Mapping[str, str]:
    out: dict[str, str] = {}
    for row in string_table:
        if not row:
            continue
        line = row[0]
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def parse_secureboot_cert(string_table: StringTable) -> Optional[SecureBootCertData]:
    kv = _parse_kv(string_table)
    if not kv:
        return None

    return SecureBootCertData(
        secureboot=kv.get("secureboot", "Unknown"),
        has_2011=int(kv.get("has_2011", "0") or "0"),
        has_2023=int(kv.get("has_2023", "0") or "0"),
        db_has_windows_uefi_ca_2023=int(kv.get("db_has_windows_uefi_ca_2023", "0") or "0"),
        kek_has_kek_2k_2023=int(kv.get("kek_has_kek_2k_2023", "0") or "0"),
    )


agent_section_secureboot_cert = AgentSection(
    name="secureboot_cert",
    parse_function=parse_secureboot_cert,
)


def discovery_secureboot_cert(section: SecureBootCertData) -> DiscoveryResult:
    yield Service(item="main")
def check_secureboot_cert(item: str, params: Mapping[str, object], section: SecureBootCertData) -> CheckResult:
    # Requested policy: CRIT when Secure Boot enabled AND 2023 cert missing.
    enforce_secureboot = bool(params.get("enforce_secureboot", False))
    require_2023_mode = str(params.get("require_2023", "any_2023"))  # any_2023 | both_specific
    warn_if_2011_present = bool(params.get("warn_if_2011_present", False))

    sb = section.secureboot

    if sb == "Unsupported":
        yield Result(state=State.OK, summary="Secure Boot unsupported (legacy BIOS / no UEFI)")
        return

    if sb != "True":
        if enforce_secureboot:
            yield Result(state=State.CRIT, summary=f"Secure Boot is {sb} (policy requires enabled)")
        else:
            yield Result(state=State.OK, summary=f"Secure Boot is {sb}")
        return

    # Secure Boot enabled
    if require_2023_mode == "both_specific":
        ok = bool(section.db_has_windows_uefi_ca_2023 and section.kek_has_kek_2k_2023)
        if ok:
            yield Result(state=State.OK, summary="Secure Boot enabled; DB+KEK 2023 certificates present")
        else:
            missing = []
            if not section.db_has_windows_uefi_ca_2023:
                missing.append("DB Windows UEFI CA 2023")
            if not section.kek_has_kek_2k_2023:
                missing.append("KEK 2K CA 2023")
            yield Result(state=State.CRIT, summary="Secure Boot enabled; missing required 2023 cert(s): " + ", ".join(missing))
    else:
        if section.has_2023:
            yield Result(state=State.OK, summary="Secure Boot enabled; 2023 certificate detected")
        else:
            yield Result(state=State.CRIT, summary="Secure Boot enabled; NO 2023 certificate detected (update needed)")

    if warn_if_2011_present and section.has_2011:
        yield Result(state=State.WARN, summary="2011 certificate still present (monitor transition)")


check_plugin_secureboot_cert = CheckPlugin(
    name="secureboot_cert",
    service_name="Secure Boot Certificate Status %s",
    discovery_function=discovery_secureboot_cert,
    check_function=check_secureboot_cert,
    check_default_parameters={
        "enforce_secureboot": False,
        "require_2023": "any_2023",
        "warn_if_2011_present": False,
    },
    check_ruleset_name="secureboot_cert",
)
