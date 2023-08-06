# Отслеживание изменений API Mediascout

## API Mediascout

https://lk.mediascout.ru/swagger/index.html

## Генератор моделей Pydantic

https://docs.pydantic.dev/datamodel_code_generator/

## Зачем?

## Как

    cd $PROJECT_ROOT
    docker run -v (pwd)/ord_mediascout_client/dtos/:/tmp/gen koxudaxi/datamodel-code-generator \
        --url https://demo.mediascout.ru/swagger/v1/swagger.json --output /tmp/gen/dtos.py
