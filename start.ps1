# Script para executar o projeto Database Indexing Benchmark

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Database Indexing Benchmark - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se o Docker está rodando
Write-Host "[1/5] Verificando Docker..." -ForegroundColor Yellow
$dockerRunning = docker ps 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker não está rodando. Por favor, inicie o Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker está rodando" -ForegroundColor Green
Write-Host ""

# Compila o projeto
Write-Host "[2/5] Compilando o projeto..." -ForegroundColor Yellow
.\mvnw.cmd clean package -DskipTests
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao compilar o projeto" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Projeto compilado com sucesso" -ForegroundColor Green
Write-Host ""

# Para containers antigos (se existirem)
Write-Host "[3/5] Parando containers antigos..." -ForegroundColor Yellow
docker-compose down -v 2>&1 | Out-Null
Write-Host "✅ Containers antigos removidos" -ForegroundColor Green
Write-Host ""

# Sobe o ambiente
Write-Host "[4/5] Subindo ambiente Docker..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao subir o ambiente" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Ambiente Docker iniciado" -ForegroundColor Green
Write-Host ""

# Aguarda inicialização
Write-Host "[5/5] Aguardando inicialização do backend..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

$attempts = 0
$maxAttempts = 30
$ready = $false

while ($attempts -lt $maxAttempts -and -not $ready) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/actuator/health" -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ready = $true
        }
    } catch {
        # Ignora erros
    }

    if (-not $ready) {
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 2
        $attempts++
    }
}

Write-Host ""

if ($ready) {
    Write-Host "✅ Backend está pronto!" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Sistema iniciado com sucesso! 🚀" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📍 Endpoints disponíveis:" -ForegroundColor Yellow
    Write-Host "   - API: http://localhost:8080" -ForegroundColor White
    Write-Host "   - Health: http://localhost:8080/actuator/health" -ForegroundColor White
    Write-Host "   - PostgreSQL: localhost:5432" -ForegroundColor White
    Write-Host ""
    Write-Host "🧪 Testar endpoint:" -ForegroundColor Yellow
    Write-Host "   curl http://localhost:8080/api/users/by-email?email=user1@example.com" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Ver logs:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs -f backend" -ForegroundColor White
    Write-Host ""
    Write-Host "🛑 Parar o ambiente:" -ForegroundColor Yellow
    Write-Host "   docker-compose down" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 Leia o QUICK_START.md para mais informações" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "⚠️  Backend demorou muito para iniciar" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Ver logs:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs backend" -ForegroundColor White
    Write-Host ""
}
