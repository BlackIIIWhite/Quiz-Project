FROM python:3.12-slim

# Install system dependencies for Python packages (including opencv dependencies)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    git \
    curl \
    libgl1 \
    libglib2.0-0 \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Rust toolchain for maturin (if you really need it)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Install maturin (needed if you build Rust extensions)
RUN pip install --upgrade pip maturin

WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy rest of the app code
COPY . /app/

# Expose port (adjust if needed)
EXPOSE 8000

# Command to run your app (adjust as needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
