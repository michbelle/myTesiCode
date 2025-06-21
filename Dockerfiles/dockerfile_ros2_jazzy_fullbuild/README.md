Docker built with

```docker build . -t rmf_all_imagev1.1```

Docker save image

```docker image save -o rmf_backup_$(date +%Y%m%d).tar rmf_all_imagev1.1```

Docker load image

```docker image load -i rmf_backup_DATE.tar```

Docker new image

```docker build --no-cache . -t rmf_all_imagev1.1```

Docker new image

```docker build --no-cache -f Dockerfile_humble . -t sensor_humble```
