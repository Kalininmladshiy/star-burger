FROM python:3.9
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
WORKDIR /star-burger/backend
ADD backend /star-burger/backend
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "collectstatic"]
