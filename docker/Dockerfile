# ---- Python Base ----
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies safely
RUN pip install --upgrade pip setuptools wheel && \
    pip install numpy==1.26.4 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose API port
EXPOSE 8000

# Command to start the app
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
