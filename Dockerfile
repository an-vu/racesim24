FROM python:3.12-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a working directory inside the container
WORKDIR .

# Copy the current directory's contents into the container's working directory
COPY . .

# Install any dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your Python script (modify as per your script)
CMD ["python", "frontend/flask/routes.py"]
