# Quick Demo Runner
# Executes the Jupyter notebook and generates all results

Write-Host "================================" -ForegroundColor Cyan
Write-Host "RAPTOR Synthetic Image Generation" -ForegroundColor Cyan
Write-Host "Proof-of-Concept Demo" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "[OK] Virtual environment is active" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Virtual environment not activated" -ForegroundColor Yellow
    Write-Host "Activating venv..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

Write-Host ""
Write-Host "Running demo notebook..." -ForegroundColor Cyan
Write-Host "This will generate:"
Write-Host "  - Simulated medical images"
Write-Host "  - Train PCA-based generator"
Write-Host "  - Generate 15 synthetic images"
Write-Host "  - Compute quality metrics"
Write-Host "  - Create result visualizations"
Write-Host ""
Write-Host "Estimated time: 3-5 minutes" -ForegroundColor Yellow
Write-Host ""

# Run notebook
& ".\venv\Scripts\python.exe" -m jupyter nbconvert `
    --to notebook `
    --execute `
    --inplace `
    --ExecutePreprocessor.timeout=600 `
    "notebooks/demo_synthetic_generation.ipynb"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "[SUCCESS] Demo completed!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Generated files in results/:" -ForegroundColor Cyan
    Get-ChildItem -Path "results" -Filter "*.png" | ForEach-Object { Write-Host "  - $($_.Name)" }
    Get-ChildItem -Path "results" -Filter "*.csv" | ForEach-Object { Write-Host "  - $($_.Name)" }
    Write-Host ""
    Write-Host "To view the notebook:" -ForegroundColor Cyan
    Write-Host "  jupyter lab notebooks/demo_synthetic_generation.ipynb"
} else {
    Write-Host ""
    Write-Host "[ERROR] Demo failed with exit code $LASTEXITCODE" -ForegroundColor Red
    Write-Host "Check the notebook for errors." -ForegroundColor Red
}
