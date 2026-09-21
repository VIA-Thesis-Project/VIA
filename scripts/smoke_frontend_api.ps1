param(
    [Parameter(Mandatory = $false)]
    [string]$API_BASE_URL = $(if ($env:API_BASE_URL) { $env:API_BASE_URL } else { "http://localhost:8000" }),

    [Parameter(Mandatory = $false)]
    [string]$EvaluationId
)

$ErrorActionPreference = "Stop"
$base = $API_BASE_URL.TrimEnd("/")

function Invoke-ReadOnlyCheck {
    param(
        [string]$Label,
        [string]$Path,
        [int[]]$AllowedStatus = @(200)
    )

    try {
        $response = Invoke-WebRequest -Uri "$base$Path" -Method Get -UseBasicParsing
        if ($AllowedStatus -notcontains [int]$response.StatusCode) {
            throw "$Label returned unexpected HTTP $($response.StatusCode)."
        }
        Write-Host "OK  $Label ($($response.StatusCode))"
    }
    catch {
        if ($_.Exception.Response) {
            $status = [int]$_.Exception.Response.StatusCode
            if ($AllowedStatus -contains $status) {
                Write-Host "OK  $Label ($status, accepted state)"
                return
            }
        }
        throw
    }
}

Invoke-ReadOnlyCheck "health" "/health"
Invoke-ReadOnlyCheck "openapi" "/openapi.json"
Invoke-ReadOnlyCheck "projects list" "/projects"
Invoke-ReadOnlyCheck "datasets list" "/datasets"
Invoke-ReadOnlyCheck "evaluations list" "/api/v1/evaluations"
Invoke-ReadOnlyCheck "evaluation capabilities" "/api/v1/evaluation-capabilities" @(200, 503)

if ($EvaluationId) {
    Invoke-ReadOnlyCheck "evaluation status" "/api/v1/evaluations/$EvaluationId"
    Invoke-ReadOnlyCheck "evaluation result" "/api/v1/evaluations/$EvaluationId/result"
    Invoke-ReadOnlyCheck "evaluation evidence" "/api/v1/evaluations/$EvaluationId/evidence"
    Invoke-ReadOnlyCheck "evaluation limitations" "/api/v1/evaluations/$EvaluationId/limitations"
}

Write-Host "Frontend API smoke checks completed. No evaluation was created."
