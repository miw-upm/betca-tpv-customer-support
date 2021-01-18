## [Máster en Ingeniería Web por la Universidad Politécnica de Madrid (miw-upm)](http://miw.etsisi.upm.es)
## Back-end con Tecnologías de Código Abierto (BETCA).
> Aplicación TPV. Pretende ser un ejemplo práctico y real de todos los conocimientos vistos

### Tecnologías necesarias
`Python` `GitHub` `Sonarcloud` `Heroku`

## :gear: Ejecución en local
1. Ejecutar en consola: `uvicorn src.main:app --reload  --port 8083`

   * Ejecución de test por consola: `python -m unittest discover tests`
   * Funciona con MongoDB embebido: `mongomock://localhost/tpv2`
   * Cliente Web (OpenAPI): `http://localhost:8083/docs`

## :book: Documentación del proyecto
[betca-tpv: Core](https://github.com/miw-upm/betca-tpv#back-end-core).

