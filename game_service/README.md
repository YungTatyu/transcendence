# game service
## Build
```
python manage.py runserver 0.0.0.0:8001
```

## Test
```
cd .. # projectのroot dirに移動
make
docker compose exec game pytest -s -vv
```
