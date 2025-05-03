# Check if venv exists, create if not
   Write-Host "Checking for virtual environment..."
   if (-Not (Test-Path .\venv)) {
       Write-Host "Creating virtual environment..."
       python -m venv venv
   }

   # Activate virtual environment
   Write-Host "Activating virtual environment..."
   if (Test-Path .\venv\Scripts\Activate.ps1) {
       .\venv\Scripts\Activate.ps1
   } else {
       Write-Host "Error: Virtual environment activation script not found."
       exit 1
   }

   # Install dependencies
   Write-Host "Installing dependencies..."
   pip install -r requirements.txt
   if ($LASTEXITCODE -ne 0) {
       Write-Host "Error: Failed to install dependencies."
       exit 1
   }

   # Run pytest
   Write-Host "Running tests with pytest..."
   pytest -v
   $testExitCode = $LASTEXITCODE

   if ($testExitCode -eq 0) {
       Write-Host "Tests passed successfully! Building Docker image..."
       docker build -t security-header-checker:latest .
       if ($LASTEXITCODE -eq 0) {
           Write-Host "Docker image built successfully!"
       } else {
           Write-Host "Failed to build Docker image."
           exit 1
       }
   } else {
       Write-Host "Tests failed. Skipping Docker build."
       exit 1
   }