# To build the docker image
```bash
    sudo docker build -t mon-django .
```

# to run the docker image
```bash
    sudo docker run -d \
      --name mon-django \
      -p 8000:8000 \
  mon-django
```