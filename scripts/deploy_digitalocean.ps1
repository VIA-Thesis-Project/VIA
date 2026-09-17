[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$HostName,

    [Parameter(Mandatory = $true)]
    [string]$Image,

    [string]$User = "via-deploy",
    [string]$RemoteRoot = "/opt/via-deploy",
    [string]$IdentityFile
)

$ErrorActionPreference = "Stop"

if ($HostName -notmatch '^[A-Za-z0-9.-]+$') {
    throw "HostName contains unsupported characters."
}
if ($User -notmatch '^[A-Za-z0-9._-]+$') {
    throw "User contains unsupported characters."
}
if ($RemoteRoot -notmatch '^/[A-Za-z0-9._/-]+$') {
    throw "RemoteRoot must be an absolute Unix path without shell metacharacters."
}
if ($Image -notmatch '^ghcr\.io/[a-z0-9._/-]+(@sha256:[0-9a-f]{64}|:[0-9a-f]{40})$') {
    throw "Image must be a GHCR digest or full 40-character git-SHA tag."
}

$sshArguments = @()
if ($IdentityFile) {
    $resolvedIdentity = (Resolve-Path -LiteralPath $IdentityFile).Path
    $sshArguments += @("-i", $resolvedIdentity)
}
$sshArguments += "$User@$HostName"
$sshArguments += "cd '$RemoteRoot' && ./scripts/deploy_digitalocean.sh '$Image'"

& ssh @sshArguments
if ($LASTEXITCODE -ne 0) {
    throw "Remote VIA deployment failed with exit code $LASTEXITCODE."
}
