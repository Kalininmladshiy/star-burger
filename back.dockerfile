FROM python:3.9
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
WORKDIR /star-burger
COPY distance /star-burger/distance
COPY foodcartapp /star-burger/foodcartapp
COPY media /star-burger/media
COPY restaurateur /star-burger/restaurateur
COPY star_burger /star-burger/star_burger
COPY templates /star-burger/templates
COPY manage.py /star-burger
COPY requirements.txt /star-burger
RUN pip install -r requirements.txt
