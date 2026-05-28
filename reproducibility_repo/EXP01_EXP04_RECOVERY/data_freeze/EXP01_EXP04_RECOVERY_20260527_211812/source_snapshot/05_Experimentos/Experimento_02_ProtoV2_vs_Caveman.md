# Experimento 02: Proto v2 vs Caveman

## Proposito

Disenar y ejecutar una prueba controlada para saber si Proto v2 reduce la sobrecarga estructural de Proto v1.

## Hipotesis

Un protolenguaje simbolico v2, con etiquetas minimas y diccionario compacto, puede acercarse o superar al modo caveman en consumo de tokens sin perder demasiada fidelidad semantica.

## Cambios frente a Experimento 01

- Proto v1 queda fuera de la ejecucion principal.
- Proto v2 usa etiquetas de una letra.
- Caveman usa formato minimo `P/S/R/N`.
- Proto v2 limita salida a 70 palabras.
- Se compara contra valores de referencia de EXP01.

## Modos

- `natural`: baseline humano, maximo 140 palabras.
- `caveman`: comprimido, maximo 90 palabras.
- `proto_v2`: simbolico compacto, maximo 70 palabras.
- `proto_v2_translated`: traduccion humana de Proto v2, maximo 120 palabras.

## Criterios de exito

Proto v2 prometedor:

- consume menos tokens que Proto v1;
- se acerca a caveman o lo supera;
- fidelidad semantica >= 4.5;
- utilidad >= 4.5;
- ambiguedad <= 1.5;
- perdida_informacion <= 1.5.

Proto v2 traducido aceptable:

- consume menos que Proto v1 traducido;
- fidelidad semantica >= 4.3;
- claridad >= 4.5;
- no pierde demasiada informacion.

## Estado

PENDIENTE_DE_EJECUCION al crear el diseno. Los resultados reales van en `../06_Resultados/Experimento_02_Resultados.md`.

## Proximos pasos

- Ejecutar piloto.
- Ejecutar tanda completa si piloto pasa.
- Comparar contra EXP01.
