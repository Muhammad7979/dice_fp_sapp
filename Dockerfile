FROM python:3.11-slim

WORKDIR /server-app
COPY /app /server-app

# Install Flask
RUN pip install flask

# Expose port
EXPOSE 5000

# Run Flask server
CMD ["python", "server.py"]