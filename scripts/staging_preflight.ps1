param(
    [switch]$Json
)

$ErrorActionPreference = "Stop"

$commands = @(
    "gcloud",
    "supabase",
    "wrangler",
    "doctl",
    "gh",
    "docker",
    "git"
)

$credentials = @(
    "GOOGLE_APPLICATION_CREDENTIALS",
    "SUPABASE_ACCESS_TOKEN",
    "CLOUDFLARE_API_TOKEN",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "DIGITALOCEAN_ACCESS_TOKEN",
    "GHCR_TOKEN"
)

$commandStatus = [ordered]@{}
foreach ($name in $commands) {
    $resolved = Get-Command $name -ErrorAction SilentlyContinue
    $commandStatus[$name] = [bool]$resolved
}

$credentialStatus = [ordered]@{}
foreach ($name in $credentials) {
    $value = [Environment]::GetEnvironmentVariable($name)
    $credentialStatus[$name] = -not [string]::IsNullOrWhiteSpace($value)
}

$dockerEngine = $false
if ($commandStatus["docker"]) {
    try {
        docker info --format "{{.ServerVersion}}" *> $null
        $dockerEngine = ($LASTEXITCODE -eq 0)
    }
    catch {
        $dockerEngine = $false
    }
}

$result = [ordered]@{
    generated_at = (Get-Date).ToUniversalTime().ToString("o")
    commands = $commandStatus
    credential_environment = $credentialStatus
    docker_engine_reachable = $dockerEngine
}

if ($Json) {
    $result | ConvertTo-Json -Depth 4
    exit 0
}

Write-Output "VIA staging preflight"
Write-Output ""
Write-Output "Commands:"
foreach ($entry in $commandStatus.GetEnumerator()) {
    Write-Output ("  {0,-12} {1}" -f $entry.Key, $(if ($entry.Value) { "present" } else { "missing" }))
}

Write-Output ""
Write-Output "Credential environment (values are never printed):"
foreach ($entry in $credentialStatus.GetEnumerator()) {
    Write-Output ("  {0,-32} {1}" -f $entry.Key, $(if ($entry.Value) { "present" } else { "absent" }))
}

Write-Output ""
Write-Output ("Docker engine reachable: {0}" -f $(if ($dockerEngine) { "yes" } else { "no" }))
