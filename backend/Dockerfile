FROM python:3.10-slim

# Set the working directory to the container
WORKDIR /app

# Copy the necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all the code of the app
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
