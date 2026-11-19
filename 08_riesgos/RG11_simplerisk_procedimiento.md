# Registro en SimpleRisk · Paso C

COOPAC Frontera Sur · Grupo 4. Procedimiento para cargar en SimpleRisk los riesgos de valor ≥ 12
(`RG08_simplerisk_carga.csv`: 12 riesgos) con su tratamiento de `RG04_tratamiento.csv`.

## 1. Levantar el entorno

```bash
cd 08_riesgos
cp .env.example .env        # cambiar las tres claves; .env no se versiona
docker compose up -d
docker compose ps           # db "healthy" y simplerisk "running"
```

Abrir `http://127.0.0.1:8084` e ingresar con el usuario `grupo4` y la clave de `SR_ADMIN_PASSWORD`.

## 2. Configurar antes de cargar riesgos

| Configuración | Valor | Fuente |
|---|---|---|
| Fórmula de riesgo | Clásica: probabilidad × impacto | RG01 |
| Escala de probabilidad 1–5 | Nombres y definición operativa de RG01 | RG01, tabla P |
| Escala de impacto 1–5 | Efecto sobre la ejecución del plan | RG01, tabla I |
| Criterio de aceptación | ≤ 6 aceptable documentado · 7–14 tratamiento con plazo · ≥ 15 decisión de Gerencia General | RG01 |
| Categorías | Las nueve del método | RG01 |
| Dueños | Por cargo, nunca por nombre | RG04, columna Responsable |

## 3. Cargar los 12 riesgos ≥ 12

Por cada fila de `RG08_simplerisk_carga.csv`: asunto `R-xx` + resumen, categoría, dueño por cargo,
probabilidad e impacto, y en la mitigación: decisión, acciones, plazo, señal temprana y umbral de `RG04`.
SimpleRisk Community no importa CSV; la carga es manual.

## 4. Capturas para `evidencias/S15/`

| Archivo | Qué debe verse |
|---|---|
| `SR01_formula_escalas.png` | Fórmula clásica y nombres de las escalas |
| `SR02_registro.png` | Lista de los 12 riesgos con su puntaje |
| `SR03_mitigacion_R-11.png` | Plan de mitigación del riesgo más alto |
| `SR04_mapa.png` | Mapa o reporte de riesgos por nivel |

Al terminar: `docker compose down` (los datos quedan en los volúmenes).
