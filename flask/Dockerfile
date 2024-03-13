# Menggunakan image Python 3.8
FROM python:3.8-slim

# Menetapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt /app/

# Menginstal dependencies
RUN pip install -r requirements.txt

# Menyalin sisa kode sumber aplikasi Flask ke dalam container
COPY . /app

# Menjalankan aplikasi Flask
CMD ["flask", "run", "--host=0.0.0.0"]