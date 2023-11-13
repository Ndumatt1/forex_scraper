# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Firefox and GeckoDriver dependencies
RUN apt-get update -y && \
    apt-get install -y firefox && \
    apt-get install -y wget && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.30.0-linux64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV MAIL_PASSWORD=cychheendvijetzy \
    SENDER=shoppiaonline8@gmail.com \
    RECIPIENT="ndubuisimathew8@gmail.com,jamierex@etlgr.com" \
    LOGIN_URL=https://live-forex-signals.com/en/login \
    USER_PASSWORD=AnaC1680 \
    USER_NAME=jamierex@etlgr.com \
    HOME_PAGE=https://live-forex-signals.com/en/

# Command to run on container start
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
