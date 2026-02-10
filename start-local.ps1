# Script para executar o projeto SEM Docker (PostgreSQL local)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Database Indexing - Execucao Local" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Verificando PostgreSQL..." -ForegroundColor Yellow
Write-Host "Certifique-se de que PostgreSQL esta instalado e rodando" -ForegroundColor Yellow
Write-Host "E que o banco 'benchmark_db' foi criado" -ForegroundColor White
Write-Host ""

Write-Host "[2/3] Compilando o projeto..." -ForegroundColor Yellow
.\mvnw.cmd clean package -DskipTests
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao compilar o projeto" -ForegroundColor Red
    exit 1
}
Write-Host "Projeto compilado com sucesso" -ForegroundColor Green
Write-Host ""

Write-Host "[3/3] Iniciando o backend..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend iniciando..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "O backend estara disponivel em:" -ForegroundColor Yellow
Write-Host "   - API: http://localhost:8080" -ForegroundColor White
Write-Host "   - Health: http://localhost:8080/actuator/health" -ForegroundColor White
Write-Host ""
Write-Host "Apos inicializar (~20 segundos), teste:" -ForegroundColor Yellow
Write-Host "   curl http://localhost:8080/api/users/by-email?email=user1@example.com" -ForegroundColor White
Write-Host ""
Write-Host "Para parar: Pressione Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

.\mvnw.cmd spring-boot:run
