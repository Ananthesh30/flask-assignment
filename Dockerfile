FROM python:3.9.7
RUN mkdir -p flask_project
WORKDIR /flask_project
COPY . /flask_project
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]

