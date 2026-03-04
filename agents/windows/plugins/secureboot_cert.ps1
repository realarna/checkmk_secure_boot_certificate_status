# Checkmk Windows Agent Plugin
# Reports Secure Boot state and checks for Microsoft Secure Boot certs (2011 vs 2023)
# Output section: <<<secureboot_cert>>>

function Write-KV($k, $v) {
    Write-Output ("{0}={1}" -f $k, $v)
}

# Some systems (legacy BIOS) will throw on Confirm-SecureBootUEFI
$secureBoot = $null
try {
    $secureBoot = Confirm-SecureBootUEFI -ErrorAction Stop
} catch {
    $secureBoot = "Unsupported"
}

Write-Output "<<<secureboot_cert>>>"
Write-KV "secureboot" $secureBoot

if ($secureBoot -eq $true) {
    $dbBytes = $null
    $kekBytes = $null

    try { $dbBytes  = (Get-SecureBootUEFI -Name db  -ErrorAction Stop).Bytes } catch {}
    try { $kekBytes = (Get-SecureBootUEFI -Name KEK -ErrorAction Stop).Bytes } catch {}

    $dbText  = ""
    $kekText = ""
    if ($dbBytes)  { $dbText  = [System.Text.Encoding]::ASCII.GetString($dbBytes) }
    if ($kekBytes) { $kekText = [System.Text.Encoding]::ASCII.GetString($kekBytes) }

    # Broad detection (robust across localized cert strings)
    $has2011 = ($dbText -match "2011") -or ($kekText -match "2011")
    $has2023 = ($dbText -match "2023") -or ($kekText -match "2023")

    # More specific matches (best effort)
    $hasWindowsUefiCa2023 = ($dbText -match "Windows UEFI CA 2023")
    $hasKek2k2023         = ($kekText -match "KEK 2K CA 2023") -or ($kekText -match "KEK.*2023")

    Write-KV "has_2011" ([int]$has2011)
    Write-KV "has_2023" ([int]$has2023)
    Write-KV "db_has_windows_uefi_ca_2023" ([int]$hasWindowsUefiCa2023)
    Write-KV "kek_has_kek_2k_2023" ([int]$hasKek2k2023)

    # For troubleshooting (shortened)
    Write-KV "db_len"  ($dbText.Length)
    Write-KV "kek_len" ($kekText.Length)

} else {
    # Disabled or Unsupported -> still provide keys
    Write-KV "has_2011" 0
    Write-KV "has_2023" 0
    Write-KV "db_has_windows_uefi_ca_2023" 0
    Write-KV "kek_has_kek_2k_2023" 0
    Write-KV "db_len" 0
    Write-KV "kek_len" 0
}
