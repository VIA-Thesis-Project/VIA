$ErrorActionPreference = "Stop"

$backendRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

Push-Location $backendRoot

try {
    Write-Host "== Ruff =="
    ruff check .
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host "`n== Pyright =="
    pyright
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host "`n== Import Linter =="
    lint-imports
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host "`n== Pytest =="
    pytest tests -q
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host "`nAll backend checks passed."
}
finally {
    Pop-Location
}