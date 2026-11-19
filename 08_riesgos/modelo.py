"""Registro académico prospectivo del Grupo 4; no sustituye aprobación gerencial."""
from pathlib import Path
from datetime import date
import csv, json, subprocess
from contextlib import redirect_stdout
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
EV=ROOT/'evidencias/S15'
G=ROOT/'graficos'
for path in (EV/'salidas',G):path.mkdir(parents=True,exist_ok=True)
CAT=['Presupuestal','Patrocinio','Capacidad de ejecución','Dependencia de personal clave',
     'Resistencia al cambio','Proveedor','Técnico','Normativo','De alcance']
# Texto, proyectos, P,I, fuente, justificación P/I, tratamiento, dueño, días relativos,
# costo referencial (no adicional al TCO), P/I objetivo, señal, umbral, aceptación.
DATA=[
('Presupuestal','Que la financiación no cubra las olas previstas por falta de compromiso plurianual, postergando PR-01 y PR-08 y los objetivos de protección y autoservicio.',
 'OE-01, OE-04 · PR-01, PR-08',3,4,'S13 PF02: inversión inicial propuesta S/ 1 000 000; 7.4 aprobada no entregada',
 'P3 provisional: exposición de financiación sin acuerdo plurianual acreditado; no hay serie de recortes. I4: una ola y dos objetivos quedarían comprometidos.',
 'Aprobar presupuesto por olas; validar flujo anual y mantener escenario reducido que priorice seguridad antes de expandir canales.',
 'Gerencia de Administración y Finanzas','Antes de aprobar la ola 1',3000,2,4,
 'Ola próxima sin partida aprobada','30 días antes de iniciar una ola sin aprobación presupuestal','Gerencia General'),
('Patrocinio','Que el patrocinio se interrumpa por acuerdos informales del comité, dejando decisiones del PETI sin autoridad y retrasando todos los proyectos.',
 'OE-01 a OE-05 · Todos',4,4,'Ficha B: comité sesiona sin actas; universo §4: tratamiento aprobado cuando se presenta',
 'P4 provisional: informalidad persistente del gobierno documentada; no se presume cambio de gerente. I4: bloquear hitos afecta la ola completa.',
 'Aprobar acta constitutiva del comité, suplencia de patrocinio, responsables por objetivo y calendario de decisiones.',
 'Gerencia General','Antes de aprobar el PETI',2000,2,4,
 'Sesiones sin decisión registrada','Dos sesiones consecutivas sin acta o sin patrocinador delegado','Gerencia General'),
('Dependencia de personal clave','Que la ausencia del responsable técnico o funcional detenga una entrega por conocimiento no transferido, retrasando la implantación de seguridad y continuidad.',
 'OE-01, OE-02 · PR-02, PR-03, PR-04',3,4,'Ficha B: TI 5 personas y oficial de seguridad parcial; política §4: ejecución y custodia en Jefatura TI',
 'P3 provisional: concentración de roles, sin evidencia de que solo una persona sepa ejecutar; validar suplencias. I4: su ausencia bloquearía una capacidad habilitadora.',
 'Designar suplentes, documentar procedimientos y realizar entrega cruzada con una prueba ejecutada por el suplente.',
 'Jefatura de TI','60 días desde aprobación del PETI',6000,2,3,
 'Entregable crítico sin suplente probado','Un entregable habilitador sin segunda persona capaz de ejecutarlo','Jefatura de TI'),
('Capacidad de ejecución','Que el equipo no termine los hitos por sostener demasiados proyectos en paralelo mientras atiende la operación, retrasando la hoja de ruta.',
 'OE-01 a OE-05 · Todos',4,4,'Ficha B: TI 5 personas; portafolio S13: 12 proyectos; 7.3 aprobada no entregada',
 'P4 provisional: 12 proyectos frente a 5 personas compartidas evidencia exposición, no horas disponibles medidas. I4: retraso de una ola si los habilitadores no cierran.',
 'Medir carga semanal, limitar dos proyectos simultáneos y contratar apoyo por entregable aprobado; no comprometer fechas sin capacidad.',
 'Responsable del PETI y Jefatura TI','Antes de programar cada ola',5000,2,4,
 'Sobrecarga y hitos abiertos','Más de dos proyectos simultáneos o desvío de hito mayor de 20 %','Comité de TI'),
('Resistencia al cambio','Que los usuarios no activen ni usen los controles nuevos por resistencia ya observada, impidiendo completar el despliegue de identidad y seguridad.',
 'OE-01 · PR-03, PR-04',4,4,'Ficha F: segundo factor disponible pero no activado para evitar resistencia',
 'P4 provisional: antecedente explícito de no adopción. I4: OE-01 no se cumple si controles siguen deshabilitados.',
 'Piloto con usuarios líderes, sesiones prácticas y verificación de acceso antes de ampliar el despliegue; registrar excepciones por cargo.',
 'Dueños funcionales y Jefatura TI','Antes del despliegue de PR-04',8000,2,4,
 'Activación y participación bajas','Menos de 80 % de cuentas piloto activadas tras dos semanas','Gerencia General'),
('Proveedor','Que la extensión del canal dependa de condiciones contractuales no aseguradas y el proveedor no habilite interfaces o soporte, postergando integración y autoservicio.',
 'OE-04 · PR-07, PR-08, PR-09',3,4,'Ficha C: canal del mismo proveedor del core; Ficha F: sin control de vencimientos; universo RG-08 dependencia',
 'P3 provisional: dependencia y falta de control contractual, sin incumplimiento del proveedor demostrado. I4: los dos proyectos de canal podrían detenerse.',
 'Confirmar contrato e interfaces antes del hito de compra; prueba de interoperabilidad y cláusulas de soporte, exportación y salida.',
 'Administración y Jefatura TI','60 días antes del inicio de PR-09',6000,2,4,
 'Contrato o acceso a interfaces sin confirmar','A 60 días del hito no hay contrato firmado o documentación de interfaz','Gerencia General'),
('Técnico','Que la migración de expedientes no pase la prueba de permisos y auditoría porque las carpetas actuales no registran lecturas, posponiendo la aceptación de PR-01.',
 'OE-01 · PR-01, PR-04, PR-05',4,4,'Ficha G: 1 900 expedientes consultados sin autorización; universo RG-02: no registra lecturas',
 'P4 provisional: antecedente de control insuficiente; la falla futura de migración es escenario. I4: objetivo de trazabilidad comprometido.',
 'Inventariar roles y datos; prueba de concepto con expedientes sintéticos, permisos y auditoría de lectura; no migrar masivamente sin aceptación.',
 'Jefatura TI y Gerencia de Créditos','Antes del hito de migración PR-01',12000,2,4,
 'Pruebas de autorización fallidas','Una lectura no autorizada o no trazada en la prueba de aceptación','Gerencia General'),
('Técnico','Que PR-02 no demuestre recuperación en sus metas por tomar el BIA sin validar y copias sin pruebas, retrasando su aceptación y la salida a producción.',
 'OE-02 · PR-02',4,4,'Política §5–6: BIA de practicante no aprobado; sin pruebas trimestrales ni registro; BIA06 RPO 1 h',
 'P4 provisional: ausencia de validación y pruebas documentada. I4: OE-02 puede fallar; los RTO/RPO son propuestas y no promesas existentes.',
 'Validar BIA con dueños; medir copia y restauración; probar copia aislada y escenarios por proceso; aprobar metas con resultados reales.',
 'Jefatura TI y dueños de procesos','Antes de aceptar PR-02',12000,2,4,
 'Meta sin prueba o copia incapaz de cubrir pérdida admisible','Un proceso crítico sin ensayo o cuyo intervalo de copia excede el RPO aprobado','Gerencia General'),
('Normativo','Que el plan no adapte sus entregables a exigencias aplicables por una matriz normativa sin alcance confirmado, obligando a rehacer controles y retrasar PR-03.',
 'OE-01 · PR-03',3,4,'Universo RG-01 y RG-06: cumplimiento y sanción sin plan; ficha cita SBS 504-2021; alcance a confirmar',
 'P3 provisional: normativa mencionada sin análisis de aplicabilidad; no se afirma cambio legal ocurrido. I4: rediseño afecta la ola de seguridad; sin atribuir sanción cierta.',
 'Cumplimiento valida alcance, plazos y evidencia aplicable con fuente oficial; revisión trimestral y ante cambios; actualizar criterios de aceptación.',
 'Cumplimiento y Riesgos','Antes de aprobar alcance PR-03 y cada trimestre',5000,2,3,
 'Requisito aplicable sin trazabilidad','Una obligación nueva o cambio aplicable sin proyecto y responsable en 15 días','Gerencia General'),
('De alcance','Que las solicitudes adicionales entren sin caso de negocio ni evaluación de dependencias, consumiendo recursos destinados a los habilitadores del PETI.',
 'OE-01 a OE-05 · Todos',3,3,'S13: 12 proyectos; control de admisión con dos fusiones; aprobación de 7.1 pendiente',
 'P3 provisional: regla propuesta aún sin aprobación; no hay histórico de cambios no autorizados. I3: un proyecto podría reducir alcance o postergarse.',
 'Aplicar control de admisión, identificar costos y dependencias de cada cambio y exigir decisión del comité antes de iniciarlo.',
 'Comité de TI','Continuo desde aprobación',2000,2,3,
 'Proyecto o entregable no registrado','Un cambio iniciado sin caso de negocio y aprobación','Comité de TI'),
('Patrocinio','Que el PETI se apruebe y quede archivado por no designar responsable ni seguimiento formal, abandonando la ejecución del conjunto del plan.',
 'OE-01 a OE-05 · Todos',4,5,'Ficha E: PETI nunca formulado; Ficha B: comité sin actas; universo §4 sin apetito escrito',
 'P4 provisional: debilidad de gobierno observada; archivo del PETI es escenario de ejecución. I5: abandono completo del plan según escala.',
 'Condicionar aprobación a responsable formal, calendario de seguimiento y tablero; primera sesión con acta y revisión de hitos.',
 'Gerencia General','En el acto de aprobación',3000,2,5,
 'Seguimiento no realizado','Un trimestre sin sesión documentada o sin responsable designado','Gerencia General'),
('Presupuestal','Que la operación de los entregables no tenga financiación recurrente porque se apruebe solo la inversión inicial, forzando a reducir servicios del PETI en años 2 y 3.',
 'OE-01, OE-02, OE-04 · PR-01, PR-02, PR-08',3,4,'S13: operación anual propuesta S/ 220 000; costo inicial S/ 1 000 000; matriz 7.4 no entregada',
 'P3 provisional: costo recurrente estimado sin asignación anual aprobada. I4: dejar servicios sin sostén frustra objetivos, no se suma la exposición a R-01.',
 'Aprobar operación y salida por año, descontar partidas solapadas del presupuesto base y revisar financiación antes de cada despliegue.',
 'Administración y Finanzas','Antes de comprometer cada proyecto',4000,2,4,
 'OPEX previsto sin partida','Cobertura aprobada del OPEX anual menor de 100 % al hito de compra','Gerencia General'),
('Capacidad de ejecución','Que los proyectos no obtengan aceptación por medir recuperación con registros contradictorios del BIA, repitiendo pruebas y demorando el cierre.',
 'OE-02, OE-05 · PR-02, PR-11',4,3,'Política §5 tiene fechas de pruebas; §6 niega pruebas trimestrales y registro. Tres de seis filas BIA sin fecha',
 'P4 provisional: contradicción documental concreta, fechas no equivalen a actas. I3: rehacer pruebas afecta alcance y fecha de un proyecto.',
 'Solicitar actas por fecha; conciliar inventario, proceso y sistema; marcar fecha sin acta como no acreditada; nueva prueba con criterio firmado.',
 'Dueños de procesos y Jefatura TI','30 días desde aprobación',4000,2,3,
 'Fecha del BIA sin evidencia recuperable','Una fecha de prueba sin acta o sin resultado verificable','Comité de TI'),
('Resistencia al cambio','Que no se complete el piloto de autoservicio por falta de validación con socios y agencias, manteniendo procesos paralelos y postergando PR-08.',
 'OE-04 · PR-08, PR-10',3,3,'Ficha A: 21 400 socios y agencias; S13 PR-10 adopción asistida propuesta; encuesta 2.4 no entregada',
 'P3 provisional: heterogeneidad de usuarios sin medición de adopción; no se inventa porcentaje actual. I3: piloto podría reducir alcance o requerir una nueva iteración.',
 'Diseñar piloto asistido accesible, criterios de éxito y registro de finalización por canal; mantener atención alternativa mientras se valida.',
 'Gerencia de Atención al Socio','Antes de ampliar PR-08',8000,2,3,
 'Trámites piloto abandonados','Finalización menor de 60 % de solicitudes elegibles durante dos semanas','Gerencia de Atención al Socio'),
]

def writecsv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def md(path,txt):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(txt.strip()+'\n',encoding='utf-8')
def nivel(v):return 'Crítico' if v>=15 else 'Alto' if v>=12 else 'Medio' if v>6 else 'Bajo'
def preparar():
    rows=[];treat=[];comm=[]
    for i,(cat,risk,projects,p,impact,source,why,action,owner,deadline,cost,pr,ir,signal,threshold,accept) in enumerate(DATA,1):
        id=f'R-{i:02}'
        rows.append(dict(id=id,Categoría=cat,Riesgo=risk,Proyectos=projects,Origen=source,
            P=p,I=impact,Justificación=why,Estado='Valoración académica provisional; pendiente de validación'))
        treat.append(dict(id=id,Valor=p*impact,Decisión='Mitigar con contingencia' if i in (1,6,12) else 'Mitigar',
            Acciones=action,Responsable=owner,Plazo=deadline,Costo_estimado_PEN=cost,
            Origen_costo='Asignación de trabajo referencial; validar dentro del TCO S13, no sumar automáticamente',
            P_residual=pr,I_residual=ir,Valor_residual=pr*ir,
            Supuesto_residual='Objetivo si tratamiento implantado y probado; sin efectividad demostrada',
            Señal_temprana=signal,Umbral_alerta=threshold,Acepta=accept,Firma='PENDIENTE'))
        comm.append(dict(id_riesgo=id,Qué_se_comunica=f'{id}: avance del tratamiento, '+signal.lower()+', residual objetivo y evidencia',
            A_quién=accept,Cuándo='Mensual y al alcanzar el umbral; semanal durante piloto' if i in (5,7,14) else 'Mensual y al alcanzar el umbral; trimestral al comité',
            Canal='Comité con acta; alerta escrita al superar umbral',Quién_comunica=owner,
            Formato='Ficha de riesgo con indicador, umbral, acción y decisión',Decisión='Escalar, reasignar recursos o detener el hito; aceptación solo con firma'))
    comm.append(dict(id_riesgo='Todos ≥ 15 / residual > 6',Qué_se_comunica='Riesgo inherente, acciones, residual estimado y decisión pendiente',
        A_quién='Gerencia General y dueños del riesgo',Cuándo='Antes de aprobar el PETI y en cada hito afectado',
        Canal='Sesión formal con acta',Quién_comunica='Responsable del PETI',
        Formato='Anexo de aceptación individual con firmas',Decisión='Aprobar, exigir más controles o posponer; nunca aceptación tácita'))
    assert set(x['Categoría'] for x in rows)==set(CAT)
    writecsv(BASE/'RG02_registro.csv',rows);writecsv(BASE/'RG04_tratamiento.csv',treat);writecsv(BASE/'RG06_comunicacion.csv',comm)
    return rows,treat,comm

def evaluar():
    df=pd.read_csv(BASE/'RG02_registro.csv')
    assert len(df)>=12 and df.id.is_unique and df.P.between(1,5).all() and df.I.between(1,5).all()
    assert set(df['Categoría'])==set(CAT)
    df['Valor']=df.P*df.I;df['Nivel']=df.Valor.map(nivel)
    df.to_csv(BASE/'RG03_evaluado.csv',index=False,encoding='utf-8-sig')
    print('EVALUACIÓN PROVISIONAL DEL GRUPO 4')
    print(f'{len(df)} riesgos; {df["Categoría"].nunique()} de 9 categorías. P e I son ordinales, no probabilidades medidas.')
    print(df[['id','Categoría','P','I','Valor','Nivel']].to_string(index=False))
    print('\nDecisión de Gerencia General (≥15): '+', '.join(df.loc[df.Valor>=15,'id']))
    matrix=np.array([[p*i for i in range(1,6)] for p in range(1,6)])
    fig,ax=plt.subplots(figsize=(9,6.5))
    from matplotlib.colors import ListedColormap,BoundaryNorm
    cmap=ListedColormap(['#d9ead3','#ffe599','#f6b26b','#e78686'])
    ax.imshow(matrix,origin='lower',cmap=cmap,norm=BoundaryNorm([.5,6.5,11.5,14.5,25.5],4))
    for p in range(1,6):
        for imp in range(1,6):
            ids=df.loc[(df.P==p)&(df.I==imp),'id'].tolist()
            ax.text(imp-1,p-1,str(p*imp),ha='center',va='center',fontsize=12,weight='bold')
            if ids:
                import textwrap
                ax.text(imp-1,p-1+.30,'\n'.join(textwrap.wrap(', '.join(ids),20)),ha='center',va='center',fontsize=8.5)
    ax.set_xticks(range(5),range(1,6));ax.set_yticks(range(5),range(1,6))
    ax.set_xlabel('Impacto sobre la ejecución del PETI');ax.set_ylabel('Probabilidad ordinal propuesta')
    ax.set_title('COOPAC Frontera Sur · Mapa de calor inherente\nEvaluación académica provisional')
    fig.tight_layout();fig.savefig(G/'RG_mapa_calor.png',dpi=160);plt.close(fig)
    return df

def residual():
    t=pd.read_csv(BASE/'RG04_tratamiento.csv')
    assert (t.Valor_residual==t.P_residual*t.I_residual).all()
    t['Reduccion_objetivo']=t.Valor-t.Valor_residual
    t['Reduccion_pct']=(100*t.Reduccion_objetivo/t.Valor).round(1)
    assert t[['Señal_temprana','Umbral_alerta','Responsable']].notna().all().all()
    assert (t.Valor_residual<=t.Valor).all()
    t.to_csv(BASE/'RG05_residual.csv',index=False,encoding='utf-8-sig')
    print(t[['id','Valor','Valor_residual','Reduccion_objetivo','Reduccion_pct','Firma']].to_string(index=False))
    total=int(t.Valor.sum());reduction=int(t.Reduccion_objetivo.sum())
    print(f'Índice ordinal agregado: {total} → {int(t.Valor_residual.sum())}; reducción OBJETIVO {reduction} puntos ({reduction/total:.1%}).')
    print('No es reducción lograda ni pérdida monetaria esperada. No sumar ordinales como probabilidad o exposición financiera.')
    high=t[t.Valor_residual>6]
    print('Residual objetivo > 6: '+', '.join(high.id))
    print('Firmas obtenidas: 0. Todos los residuales requieren validación; no se acepta ninguno en nombre de su dueño.')
    print('Sin señal temprana: 0; sin umbral: 0.')
    return t

def bia():
    b=pd.read_csv(ROOT/'bia.csv')
    f=[]
    for r in b.to_dict('records'):
        id=r['id']; process=r['proceso']
        if pd.isna(r['ultima_prueba']):
            f.append(dict(id=id,proceso=process,Hallazgo='Sin fecha de última prueba',Acción='Programar prueba y conservar acta; ausencia de fecha no demuestra ausencia de copia'))
        else:
            f.append(dict(id=id,proceso=process,Hallazgo='Fecha indicada sin acta entregada; política declara falta de pruebas trimestrales',Acción='Solicitar acta y resultado; marcar prueba no acreditada hasta verificar'))
        if r['rpo_horas']<24:
            f.append(dict(id=id,proceso=process,Hallazgo=f'RPO {r["rpo_horas"]} h frente a copia incremental diaria declarada',Acción='Medir pérdida máxima y frecuencia efectiva; una copia cada 24 h no acredita un RPO menor sin mecanismos adicionales'))
        if id=='BIA02':
            f.append(dict(id=id,proceso=process,Hallazgo='Criticidad alta e impacto a 24 h bajo con RTO 72 h',Acción='Revalidar con dueño; posible horizonte de impacto distinto, no corregir arbitrariamente'))
        if id=='BIA06':
            f.append(dict(id=id,proceso=process,Hallazgo='Criticidad media con impacto a 24 h alto',Acción='Revisar criterio de criticidad y ventanas de reporte; no suponer plazo legal'))
    writecsv(BASE/'RG00_hallazgos_bia.csv',f)
    print('BIA: 6 procesos, 3 fechas ausentes, 3 fechas sin actas entregadas. BIA sin aprobación.')
    print('RPO de 1 o 4 h no acreditado por respaldo diario. RPO > RTO no es por sí solo una contradicción.')
    for x in f:print(x['id'],x['Hallazgo'])
    return f

def generar():
    rows,ts,comm=preparar()
    for name,fn in [('RG00_bia',bia),('RG03_evaluacion',evaluar),('RG05_residual',residual)]:
        with (EV/'salidas'/f'{name}.txt').open('w',encoding='utf-8') as f,redirect_stdout(f):
            result=fn()
        if name=='RG03_evaluacion':df=result
        if name=='RG05_residual':t=result
    assert set(df.id)==set(t.id)
    assert all(r['Justificación'] and r['Origen'] and r['Proyectos'] for r in rows)
    checks=[
       '14 riesgos con evento, causa, consecuencia y proyectos propuestos vinculados.',
       '9/9 categorías cubiertas. Riesgo de archivo del plan incluido en Patrocinio.',
       '14/14 filas con justificación explícita P/I; todas provisionales. P requiere validación, no es frecuencia medida.',
       'Todo valor >6 tiene acciones, cargo, plazo, costo, señal, umbral y residual objetivo.',
       'Todos los cálculos P×I y P residual×I residual verificados; no hay IDs duplicados o faltantes.',
       'Matriz de comunicación: 8 columnas, 14 riesgos y una regla de escalamiento.',
       'Criterios versionados en commit anterior a la ejecución; no equivale a acuerdo gerencial.',
       'Firmas reales de aceptación: 0. Pre-mortem propuesto, no sesión realizada.',
    ]
    md(EV/'salidas/RG07_validacion.txt','VALIDACIÓN DEL ESCENARIO\n'+'\n'.join(f'{i}. {s}' for i,s in enumerate(checks,1)))
    writecsv(BASE/'RG08_simplerisk_carga.csv',df.loc[df.Valor>=12,['id','Categoría','Riesgo','Proyectos','P','I','Valor','Justificación']].to_dict('records'))
    md(BASE/'RG09_premortem.md',"""# Pre mortem propuesto para validar con el equipo
Supuesto de trabajo: al cierre del año 3 el PETI no entregó sus objetivos.
Este ejercicio fue elaborado documentalmente; no se afirma una sesión con participantes.

1. Finanzas: faltó operación recurrente además de la compra inicial. Contrastar R-01 y R-12 con 7.4.
2. Comité: se aprobaron hitos sin responsables ni actas. Contrastar R-02 y R-11.
3. TI: se sobrecargó al equipo y no existía suplencia probada. Contrastar R-03 y R-04.
4. Usuarios: se mantuvo la resistencia al segundo factor y no se probó el recorrido de los socios. Contrastar R-05 y R-14.
5. Proveedor: se comprometió el canal antes de asegurar interfaces y soporte. Contrastar R-06.
6. Créditos y continuidad: las pruebas no acreditaron permisos, recuperación ni RPO. Contrastar R-07, R-08 y R-13.
7. Cumplimiento: requisitos y alcance no validados obligaron a rehacer controles. Contrastar R-09.
8. Comité: se admitieron ampliaciones sin caso de negocio. Contrastar R-10.

Registrar fecha real, cargos participantes, evidencias, desacuerdos y ajustes antes de cerrar.
""")
    md(BASE/'RG10_aceptacion_residual.md',"""# Formato de decisión sobre riesgo residual
Documento sin firmas. Preparado por el Grupo 4; no constituye aceptación.

| Campo | Completar por el dueño |
|---|---|
| ID del riesgo | |
| Dueño por cargo | |
| Valor inherente | |
| Tratamiento ejecutado y evidencia | |
| P / I residual verificados | |
| Fecha, periodo y límite de aceptación | |
| Decisión | Aceptar / tratar más / posponer / evitar |
| Condiciones, señal y umbral | |
| Firma del dueño y fecha real | |
| Decisión de Gerencia General si corresponde | |

Usar una ficha por riesgo. El residual del registro es una estimación condicionada;
antes de firmar se debe verificar la efectividad del tratamiento.
""")
    initial=int(df.Valor.sum());target=int(t.Valor_residual.sum())
    crit=df.loc[df.Valor>=15,'id'].tolist();high=t.loc[t.Valor_residual>6,'id'].tolist()
    sections=[
      ('8.1 Alcance, contexto y criterios','Se evalúa ejecución del PETI en tres años relativos, no riesgos de operación. RG01 fija P e I ordinales y las bandas ≤6, 7–14 y ≥15. Se versionó antes de ejecutar. Acuerdo gerencial pendiente; las fechas del caso no son fechas de aprobación del plan.'),
      ('8.2 Método','Se sigue la secuencia de ISO 31000 como referencia metodológica: contexto, identificación, análisis, valoración, tratamiento, comunicación y revisión. Fuentes: política, BIA, universo auditable, ficha del caso y propuesta S13. El pre-mortem es documental propuesto y no acta de sesión.'),
      ('8.3 Registro de riesgos','RG02 incluye 14 escenarios sobre las nueve categorías y objetivos/proyectos propuestos. R-11 registra que el plan se apruebe y archive. Se conserva la diferencia entre un hecho de operación y su consecuencia para entregar un proyecto.'),
      ('8.4 Evaluación y mapa de calor','RG03 contiene '+str(len(df))+' valoraciones. Críticos: '+', '.join(crit)+'. Cada P e I tiene un fundamento, límites y carácter provisional; no hay una muestra para estimar frecuencias de planes comparables. El mapa visualiza productos ordinales, no pérdidas monetarias.'),
      ('8.5 Tratamiento y riesgo residual',f'RG04 cubre todos los riesgos >6. Índice ordinal agregado {initial} a {target}; reducción objetivo de {initial-target} puntos ({(initial-target)/initial:.1%}). No es reducción lograda: depende de ejecutar y probar los controles. Los costos son asignaciones referenciales que deben conciliarse con el TCO S13.'),
      ('8.6 Señales tempranas y umbrales','Cada riesgo tiene una señal observable y umbral: aprobación de partida, actas, suplencia, carga, activación, interfaces, pruebas y adopción. Cero registros sin señal ni umbral. Los umbrales son propuestas para aprobación, no tolerancias legales.'),
      ('8.7 Matriz de comunicación','RG06 define ocho columnas: ID, qué, a quién, cuándo, canal, quién comunica, formato y decisión. Incluye una fila de escalamiento antes de aprobar el plan para críticos y residuales >6. Solo se diseña el flujo: no se enviaron mensajes a terceros.'),
      ('8.8 Aceptación formal','Residuales objetivo >6: '+', '.join(high)+'. Todos tienen cargo de aceptación; firmas obtenidas: cero. Los ≤6 también requieren documentación y firma antes de calificarse como aceptados. El anexo F deja el formato sin firma para la sección 9.'),
      ('8.9 Seguimiento y revisión','Responsable propuesto: dueño por cargo y responsable PETI. Revisar trimestralmente, mensualmente para residuales >6, semanalmente en pilotos según RG06 y extraordinariamente ante umbral. Revisar vigencia del BIA y consistencia de pruebas antes de aceptar PR-02.'),
    ]
    lines=['# 8. Gestión de riesgos del plan','COOPAC Frontera Sur · Grupo 4 · evaluación académica provisional.']
    for title,txt in sections:lines.extend(['\n## '+title,txt])
    lines.extend(['\n## Registro resumido','| ID | Categoría | P | I | Valor | Residual objetivo |','|---|---|---:|---:|---:|---:|'])
    for r,z in zip(rows,ts):lines.append(f'| {r["id"]} | {r["Categoría"]} | {r["P"]} | {r["I"]} | {r["P"]*r["I"]} | {z["Valor_residual"]} |')
    lines.extend(['\n## Fuentes y pendientes',
      '- Fuentes originales en la raíz; RG00 registra hallazgos y evita cambiar el BIA sin aprobación.',
      '- Propuesta de portafolio S13 usada como trazabilidad, pendiente de contrastar con PETI aprobado.',
      '- [ISO 31000:2018](https://www.iso.org/standard/65694.html); [SimpleRisk Docker oficial](https://github.com/simplerisk/docker/tree/master/simplerisk-minimal).',
      '- Criterios, P/I, objetivos y residual requieren validación y firma reales. No se declara conformidad legal.'])
    md(BASE/'8_gestion_riesgos.md','\n\n'.join(lines))
    (BASE/'resumen.json').write_text(json.dumps(dict(registro=df.to_dict('records'),tratamiento=t.to_dict('records'),
        comunicacion=comm,secciones=sections,criticos=crit,residuales=high,inicial=initial,residual=target),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(df)} riesgos, 9 categorías, {len(crit)} críticos, {len(high)} residuales objetivo >6.')
    print(f'Índice ordinal {initial} → {target}; reducción objetivo, no lograda.')

if __name__=='__main__':generar()
