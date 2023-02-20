#
FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY . /code/app

# Set the environment variable to indicate that the script should be executed in threads
ENV EXECUTE_IN_THREADS=True

# Make port 80 available to the world outside this container
EXPOSE 80
#
CMD ["uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "5000"]
