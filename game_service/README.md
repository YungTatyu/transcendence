## Build
```
python manage.py runserver 0.0.0.0:8001
```

## Test
```
python manage.py test
#もしくは
cd .. # projectのroot dirに移動
make
docker compose exec game python manage.py test
```
