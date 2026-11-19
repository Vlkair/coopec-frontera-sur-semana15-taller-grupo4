"""Pasos C y D del taller S15 · COOPAC Frontera Sur · Grupo 4.

Paso C: decisión de tratamiento por riesgo y ajustes del tratamiento.
Paso D: matriz de comunicación específica por riesgo (ocho columnas).
modelo.py importa estos datos al generar RG04_tratamiento.csv y RG06_comunicacion.csv.
"""

# Paso C · Decisión de tratamiento (ISO 31000: evitar, mitigar, transferir, aceptar).
DECISION = {
    'R-01': 'Mitigar con contingencia',
    'R-02': 'Mitigar',
    'R-03': 'Mitigar',
    'R-04': 'Mitigar',
    'R-05': 'Mitigar',
    'R-06': 'Transferir + Mitigar',
    'R-07': 'Mitigar',
    'R-08': 'Mitigar',
    'R-09': 'Mitigar con vigilancia',
    'R-10': 'Mitigar',
    'R-11': 'Mitigar con contingencia',
    'R-12': 'Mitigar con contingencia',
    'R-13': 'Mitigar',
    'R-14': 'Mitigar',
}

# Paso C · Ajustes al tratamiento. Solo se cambia lo que el tratamiento justifica.
AJUSTE = {
    'R-06': dict(
        Acciones='Firmar contrato con niveles de servicio, penalidad por incumplimiento, derecho de auditoría y '
                 'cláusula de exportación y salida (transfiere al proveedor el costo del incumplimiento); '
                 'prueba de interoperabilidad y documentación de interfaces antes del hito de compra.',
    ),
    'R-11': dict(
        Acciones='Condicionar la aprobación a un responsable formal, calendario de seguimiento y tablero; primera '
                 'sesión con acta. Contingencia: incorporar el núcleo habilitador (PR-02, PR-03 y PR-04) al plan '
                 'operativo y al presupuesto anual, para que un archivo del PETI no detenga seguridad y continuidad.',
        I_residual=4,
        Supuesto_residual='Objetivo si tratamiento implantado y probado. I baja de 5 a 4 solo si el núcleo '
                          'habilitador queda en el plan operativo anual; sin efectividad demostrada',
    ),
}

# Paso D · Matriz de comunicación: qué, a quién, cuándo, canal, quién comunica, formato, decisión.
COMM = {
    'R-01': ('Aprobación de la partida de la próxima ola y ejecución presupuestal frente a lo planificado',
             'Gerencia General y Consejo de Administración', 'Trimestral y 30 días antes de iniciar cada ola',
             'Informe escrito al Consejo', 'Gerencia de Administración y Finanzas',
             'Reporte de 1 página con escenario reducido', 'Aprobar la ola, activar el escenario reducido o postergar'),
    'R-02': ('Asistencia del patrocinador y decisiones registradas en las actas del comité',
             'Consejo de Administración', 'Trimestral; inmediato tras dos sesiones sin acta',
             'Sesión del Consejo', 'Responsable del PETI',
             'Resumen de actas y decisiones pendientes', 'Ratificar el patrocinio o designar suplente'),
    'R-03': ('Entregables habilitadores con y sin suplente probado',
             'Gerencia General y Recursos Humanos', 'Mensual hasta que todos tengan suplente probado',
             'Correo con tablero', 'Jefatura de TI',
             'Indicador de factor bus por entregable', 'Priorizar formación, contratación o reprogramar'),
    'R-04': ('Carga semanal del área de TI, proyectos en paralelo y desvío de hitos',
             'Comité de TI', 'Mensual; alerta al superar dos proyectos simultáneos o 20 % de desvío',
             'Sesión de comité', 'Responsable del PETI',
             'Tablero de capacidad', 'Reprogramar la ola o contratar apoyo por entregable'),
    'R-05': ('Activación del segundo factor y uso de los controles por agencia en el piloto',
             'Gerencia General y jefaturas de agencia', 'Semanal durante el piloto; mensual después',
             'Reunión de seguimiento del piloto', 'Jefatura de TI con dueños funcionales',
             'Tablero de activación por agencia', 'Ampliar el despliegue, reforzar la capacitación o ajustar el diseño'),
    'R-06': ('Estado del contrato, niveles de servicio, penalidades e interfaces del proveedor',
             'Gerencia General', 'Quincenal desde 90 días antes de PR-09 hasta la firma',
             'Correo con estado del contrato', 'Gerencia de Administración y Finanzas',
             'Estado en una línea con hitos contractuales', 'Firmar, escalar la negociación o activar el plan de salida'),
    'R-07': ('Resultado de las pruebas de permisos y auditoría de lectura de expedientes',
             'Gerencia de Créditos y Comité de TI', 'Al concluir cada prueba; semanal durante la migración',
             'Sesión de comité', 'Jefatura de TI',
             'Informe técnico con lecturas no trazadas', 'Aprobar la migración de PR-01 o repetir las pruebas'),
    'R-08': ('BIA validado y RTO/RPO medidos en las pruebas de restauración frente a la meta',
             'Dueños de proceso y Gerencia General', 'Tras cada prueba y antes de aceptar PR-02',
             'Sesión de comité', 'Jefatura de TI',
             'Informe técnico por proceso', 'Aprobar las metas RTO/RPO o rediseñar PR-02'),
    'R-09': ('Obligaciones aplicables de la Res. SBS 504-2021 y brechas sin proyecto ni responsable',
             'Gerencia General y Comité de TI', 'Trimestral y ante cualquier cambio normativo',
             'Informe escrito', 'Cumplimiento y Riesgos',
             'Matriz normativa de brechas', 'Ajustar el alcance de PR-03 o asignar responsable'),
    'R-10': ('Pedidos nuevos recibidos y su decisión de admisión',
             'Comité de TI y áreas solicitantes', 'En cada pedido nuevo; resumen trimestral',
             'Sesión de comité', 'Responsable del PETI',
             'Registro de cambios con caso de negocio', 'Admitir, postergar o rechazar el pedido'),
    'R-11': ('Estado de ejecución del PETI y avance de indicadores',
             'Gerencia General y Consejo de Administración', 'Trimestral',
             'Sesión de comité con acta elevada al Consejo', 'Responsable del PETI',
             'Tablero de indicadores y acta', 'Continuar, ajustar o detener el plan'),
    'R-12': ('Cobertura del OPEX anual de los servicios ya entregados',
             'Gerencia General y Gerencia de Administración y Finanzas', 'Al formular el presupuesto anual y antes de cada compra',
             'Informe escrito', 'Gerencia de Administración y Finanzas',
             'Proyección de OPEX por año', 'Aprobar la compra, reducir el alcance o buscar financiación'),
    'R-13': ('Actas de prueba del BIA conciliadas y fechas no acreditadas',
             'Comité de TI y dueños de proceso', 'Mensual hasta conciliar; luego en cada prueba',
             'Correo con matriz de conciliación', 'Jefatura de TI',
             'Matriz de conciliación del BIA', 'Repetir la prueba o aceptar la evidencia'),
    'R-14': ('Finalización de trámites del piloto de autoservicio por canal y agencia',
             'Gerencia de Atención al Socio y jefaturas de agencia', 'Semanal durante el piloto; mensual después',
             'Reunión de equipo', 'Gerencia de Atención al Socio',
             'Tablero de finalización de trámites', 'Ampliar PR-08, rediseñar o mantener la atención asistida'),
}

ESCALAMIENTO = ('Todos ≥ 15 / residual > 6',
                'Riesgo inherente, acciones, residual estimado y responsable de la aceptación',
                'Gerencia General, Consejo de Administración y dueños del riesgo',
                'Antes de aprobar el PETI y en cada hito afectado', 'Sesión formal con acta',
                'Responsable del PETI', 'Anexo de aceptación individual con firmas',
                'Aprobar el plan con conocimiento del riesgo, exigir más controles o posponer; nunca aceptación tácita')

COLUMNAS = ['id_riesgo', 'Qué_se_comunica', 'A_quién', 'Cuándo', 'Canal', 'Quién_comunica', 'Formato', 'Decisión']


def fila_comunicacion(id_riesgo):
    return dict(zip(COLUMNAS, (id_riesgo, *COMM[id_riesgo])))


def fila_escalamiento():
    return dict(zip(COLUMNAS, ESCALAMIENTO))
