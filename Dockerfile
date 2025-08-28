FROM python:3.11-slim

WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git

# Copy the rendergit source code
COPY vendor/rendergit /app/rendergit

# Copy the mcp server code
COPY mcp_rendergit.py /app/

# Add rendergit to PYTHONPATH
ENV PYTHONPATH="/app/rendergit"

# Install dependencies
RUN pip install markdown pygments flask flask-cors gunicorn

# Expose the port the MCP server will run on
EXPOSE 8080

# Command to run the MCP server with Gunicorn and detailed logging  
CMD ["gunicorn", "--workers", "1", "--threads", "4", "--bind", "0.0.0.0:8080", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "mcp_rendergit:app"]
