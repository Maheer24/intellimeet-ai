FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=""

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip

# Step 1: Install all packages except torch and sentence-transformers
RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    httpx==0.27.0 \
    supabase==2.10.0 \
    nltk==3.8.1 \
    scipy==1.13.1 \
    Pillow==10.2.0 \
    sentencepiece==0.1.99 \
    uvicorn==0.27.1 \
    python-dotenv==1.0.1 \
    pandas==2.2.2 \
    python-multipart==0.0.9 \
    pydantic==2.6.4 \
    groq \
    pinecone \
    scikit-learn==1.4.2 \
    numpy==1.26.4 \
    huggingface-hub==0.21.4 \
    transformers==4.36.2 \
    tokenizers==0.15.2 

# Step 2: Install CPU-only torch explicitly
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.2.2+cpu \
    torchvision==0.17.2+cpu

# Step 3: Install sentence-transformers without letting it override torch
RUN pip install --no-cache-dir --no-deps \
    sentence-transformers==2.2.2

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]