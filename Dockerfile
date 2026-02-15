# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (build tools for some python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run run_spiders.py first to populate DB, then launch Streamlit
CMD python run_spiders.py && streamlit run app.py --server.port=8501 --server.address=0.0.0.0
