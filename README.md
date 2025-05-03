
# Security Header Checker

## Introduction

Security Header Checker is a Flask-based tool to check the security headers of a website and report vulnerabilities. It automates the process of testing and building the application, including Docker containerization for easy deployment.

## Files and Setup

* **app.py**: The main Flask application.
* **Dockerfile**: Defines the Docker image for the application.
* **build.ps1**: PowerShell script that automates the build pipeline, including testing and Docker image creation.
* **requirements.txt**: Lists the Python dependencies required to run the app.
* **test\_app.py**: Contains pytest tests for the Flask application.

### Build and Run

The project comes with an automated build pipeline. To set up and run the application:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/security-header-checker.git
   ```

2. **Run the build pipeline** (which includes testing and Docker build):

   * On Windows (PowerShell):

     ```bash
     .\build.ps1
     ```
   * This script will:

     * Install dependencies from `requirements.txt`.
     * Run pytest tests (`test_app.py`).
     * Build the Docker image using the `Dockerfile`.

3. **Run the Docker container**:
   After the build completes, run the Docker container:

   ```bash
   docker run -p 5000:5000 security-header-checker
   ```

   The Flask app will be available at `http://localhost:5000`.

## Testing

To run tests manually, execute the following:

```bash
pytest test_app.py
```
