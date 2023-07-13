# Use the Miniconda3 base image with Python 3.10.10
FROM continuumio/miniconda3:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the Django project files to the container
COPY . .

# Create a Conda environment and install dependencies
RUN conda create -y --name myenv python=3.10.10 && \
    echo "conda activate myenv" >> ~/.bashrc && \
    /bin/bash -c "source ~/.bashrc && pip install --no-cache-dir -r requirements.txt"

# Expose the default Django development server port (change if necessary)
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

