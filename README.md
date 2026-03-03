# 🔐 Windows Secure Boot Certificate Status (Checkmk Extension)

![Checkmk](https://img.shields.io/badge/Checkmk-2.4+-blue) ![Windows
Server](https://img.shields.io/badge/Windows%20Server-2016%2B-green)
![Agent
Bakery](https://img.shields.io/badge/Agent%20Bakery-Supported-success)
![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey)

Monitor Microsoft Secure Boot 2023 certificate rollout status on Windows
Server systems using Checkmk.

------------------------------------------------------------------------

## 📖 Overview

This Checkmk extension monitors the Secure Boot certificate state on:

-   Windows Server 2016\
-   Windows Server 2019\
-   Windows Server 2022\
-   Windows Server 2025

It verifies whether the **Microsoft 2023 Secure Boot certificates** are
installed and alerts if systems are still relying on the legacy 2011
certificates.

The extension includes:

-   ✅ Agent-based check (`cmk.agent_based.v2`)\
-   ✅ Check parameter ruleset (`cmk.rulesets.v1`)\
-   ✅ Agent Bakery integration\
-   ✅ Windows PowerShell agent plugin

------------------------------------------------------------------------

## 🚨 Why This Plugin Is Needed

Microsoft is replacing the original Secure Boot certificates issued in
2011.

These certificates expire in **2026**.

Windows Server **does NOT automatically activate** the 2023 certificates
--- administrators must explicitly trigger the update.

Without the 2023 certificates:

-   Future Secure Boot updates may fail\
-   Systems may enter a degraded security state\
-   Compliance checks may fail\
-   Hardened environments may block boot validation

This plugin provides:

-   Central visibility of rollout status\
-   Compliance monitoring\
-   Baseline enforcement\
-   Verification after update

------------------------------------------------------------------------

## 🔎 What the Plugin Checks

The plugin evaluates:

1.  Secure Boot state\
2.  Presence of 2023 certificates in:
    -   UEFI DB\
    -   UEFI KEK

### 📊 Result Logic

  Condition                                        State
  ------------------------------------------------ ------------------------------------
  Secure Boot enabled + 2023 certificate present   🟢 OK
  Secure Boot enabled + 2023 certificate missing   🔴 CRIT
  Secure Boot disabled                             🟢 OK (unless enforcement enabled)
  Legacy BIOS / Unsupported                        🟢 OK

------------------------------------------------------------------------

## 🛠 Installation

### 1️⃣ Install the MKP

``` bash
su - <site>
cmk -P install windows_secureboot_cert-<version>.mkp
cmk -R
```

------------------------------------------------------------------------

### 2️⃣ Enable Agent Deployment (Bakery)

Navigate to:

    Setup → Agents → Agent rules

Create the rule:

> **Secure Boot certificate agent plugin (Windows)**

Select:

✔ Deploy the plugin

Assign the rule to: - Specific hosts\
- Folders\
- Host tags

Then:

    Bake new agent
    Deploy to Windows host

The following file will be included in the baked agent:

    plugins\secureboot_cert.ps1

------------------------------------------------------------------------

### 3️⃣ Discover the Service

Run **Service Discovery** on the host.

The following service will appear:

    Secure Boot Certificate Status

------------------------------------------------------------------------

## ⚙ WATO / Setup Rules

The extension provides **two rule types**.

------------------------------------------------------------------------

## 1️⃣ Check Parameter Rule

Location:

    Setup → Services → Service monitoring rules

Rule name:

> **Secure Boot certificate status (Windows Server)**

This rule controls evaluation behavior.

### 🔐 Enforce Secure Boot enabled

If enabled:

-   Secure Boot disabled → 🔴 CRIT

If disabled (default):

-   Secure Boot disabled → 🟢 OK

Use this option when Secure Boot is mandatory in your security baseline.

------------------------------------------------------------------------

### 🏷 2023 Certificate Detection Mode

#### ✔ At least one 2023 certificate detected (recommended)

More tolerant and firmware-agnostic.\
Recommended for production environments.

#### ✔ Require both DB and KEK 2023

Stricter validation requiring:

-   Windows UEFI CA 2023 (DB)\
-   Microsoft KEK 2K CA 2023 (KEK)

Use for hardened or compliance-driven environments.

------------------------------------------------------------------------

### ⚠ Warn if 2011 certificate still present

Adds a warning during migration if legacy certificates remain.

Useful during staged rollouts.

------------------------------------------------------------------------

## 2️⃣ Agent Bakery Rule

Location:

    Setup → Agents → Agent rules

Rule name:

> **Secure Boot certificate agent plugin (Windows)**

This rule controls deployment of the Windows PowerShell plugin.

Without this rule: - The check exists\
- But the plugin is not included in baked agents

------------------------------------------------------------------------


## 🧩 Design Characteristics

-   Single service per host\
-   Auto-discovery based\
-   No SNMP dependencies\
-   No external modules required\
-   Pure PowerShell + native SecureBootUEFI API

------------------------------------------------------------------------

## 👤 Author

**Ahmet Arnautovic**\
ahmet.arnautovic@acp.at

------------------------------------------------------------------------


## 📜 License

This project is licensed under the **Creative Commons Attribution 4.0
International (CC BY 4.0)** License.

You are free to:

-   Share --- copy and redistribute the material in any medium or
    format\
-   Adapt --- remix, transform, and build upon the material

For any purpose, even commercially, under the following terms:

-   Attribution --- You must give appropriate credit.

Full license text available at:\
https://creativecommons.org/licenses/by/4.0/


