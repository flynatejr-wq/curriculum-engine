# LessonGrove local dev startup
# Loads backend .env, starts FastAPI + Vite in parallel

$Root = $PSScriptRoot

# Load backend .env into current session
$envFile = Join-Path $Root "backend\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+?)\s*=\s*(.*)\s*$') {
            $name  = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host "Loaded .env from backend/.env"
} else {
    Write-Warning "backend/.env not found — make sure ANTHROPIC_API_KEY is set in your environment"
}

# Start FastAPI backend
$backendDir = Join-Path $Root "backend"
Start-Process -FilePath "python" `
    -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" `
    -WorkingDirectory $backendDir `
    -NoNewWindow
Write-Host "Backend started on http://localhost:8000"

# Start Vite frontend
$frontendDir = Join-Path $Root "frontend"
Start-Process -FilePath "cmd" `
    -ArgumentList "/c", "cd `"$frontendDir`" && npm run dev" `
    -NoNewWindow
Write-Host "Frontend starting on http://localhost:5173"

Write-Host ""
Write-Host "LessonGrove is running. Press Ctrl+C to stop."
Wait-Event
