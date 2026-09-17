[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourcePath,

    [Parameter(Mandatory = $true)]
    [string]$HostName,

    [string]$User = "via-deploy",
    [string]$RemotePath = "/srv/via/sources",
    [string]$IdentityFile
)

$ErrorActionPreference = "Stop"

if ($HostName -notmatch '^[A-Za-z0-9.-]+$') {
    throw "HostName contains unsupported characters."
}
if ($User -notmatch '^[A-Za-z0-9._-]+$') {
    throw "User contains unsupported characters."
}
if ($RemotePath -notmatch '^/[A-Za-z0-9._/-]+$') {
    throw "RemotePath must be an absolute Unix path without shell metacharacters."
}

$resolvedSource = (Resolve-Path -LiteralPath $SourcePath).Path
if (-not (Test-Path -LiteralPath $resolvedSource -PathType Container)) {
    throw "SourcePath must name an existing directory."
}
if (-not (Get-ChildItem -LiteralPath $resolvedSource -Force | Select-Object -First 1)) {
    throw "SourcePath is empty."
}

$target = "$User@$HostName"
$identityArguments = @()
if ($IdentityFile) {
    $resolvedIdentity = (Resolve-Path -LiteralPath $IdentityFile).Path
    $identityArguments = @("-i", $resolvedIdentity)
}

& ssh @identityArguments $target "test -d '$RemotePath' && test -w '$RemotePath'"
if ($LASTEXITCODE -ne 0) {
    throw "Remote scientific source directory is missing or not writable."
}

$copySource = Join-Path $resolvedSource "."
& scp @identityArguments -r $copySource "$target`:$RemotePath/"
if ($LASTEXITCODE -ne 0) {
    throw "Scientific source upload failed with exit code $LASTEXITCODE."
}

$permissionCommand = (@'
set -eu
chmod 0755 '__REMOTE_PATH__'
find '__REMOTE_PATH__' -mindepth 1 -type d -exec chmod 0755 {} +
find '__REMOTE_PATH__' -type f -exec chmod 0644 {} +
if find '__REMOTE_PATH__' -type d ! -perm 0755 -print -quit | grep -q .; then
    echo "Scientific source directory permissions are not exactly 0755." >&2
    exit 1
fi
if find '__REMOTE_PATH__' -type f ! -perm 0644 -print -quit | grep -q .; then
    echo "Scientific source file permissions are not exactly 0644." >&2
    exit 1
fi
'@).Replace('__REMOTE_PATH__', $RemotePath)

& ssh @identityArguments $target $permissionCommand
if ($LASTEXITCODE -ne 0) {
    throw "Scientific source permission normalization or verification failed."
}

Write-Host (
    "Copied scientific sources to $target`:$RemotePath and enforced " +
    "directories 0755 / files 0644."
)
