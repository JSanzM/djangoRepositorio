import csv

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl.styles import Font, PatternFill

from .forms import CdsForm
from .models import Cds, Grupo, Tipo


# Create your views here.
def cds_listar(request):
    cds = Cds.objects.all()
    return render(request, 'cds/cds_listar.html', {'cds': cds,})

def cds_alta_cd(request):

    if request.method == 'POST':
        formulario = CdsForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('cds:cds')
    else:
        formulario = CdsForm()

    contexto = {
        'formulario': formulario,
    }
    return render(request, 'cds/editar_cd.html', contexto)

def cds_buscar_cd(request):
    resultado = None

    if request.method == 'GET':
        titulo = request.GET.get('titulo', '').strip()
        grupo = request.GET.get('grupo', '').strip()

        if grupo or titulo:
            query = Q()

            if grupo:
                query &= Q(grupo__icontains=grupo)
            if titulo:
                query &= Q(titulo__icontains=titulo)

            resultado = Cds.objects.filter(query)

    contexto = {
        'resultado': resultado,
        'grupo_buscar': request.GET.get('grupo', ''),
        'titulo_buscar': request.GET.get('titulo', ''),
    }
    return render(request, 'cds/buscar_cds.html', contexto)

def cds_importar_cds(request):
    """
        Importa cds desde un archivo CSV
    """
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']

        # Decodificar CSV UTF-8
        import io
        decoded_file = io.TextIOWrapper(archivo.file, encoding='utf-8')
        reader = csv.reader(decoded_file)

        # Saltar encabezado si existe
        next(reader, None)

        contador = 0
        errors = []

        for row in reader:
            try:
                grupo = Grupo.objects.filter(grupo=row[2]).first()
                tipo = Tipo.objects.filter(tipo=row[6]).first()
                Cds.objects.create(
                        titulo=row[1],
                        grupo=grupo,
                        anyo=int(row[3]),
                        copiado=row[4],
                        falta=row[5],
                        tipo=tipo,
                        notas=row[7] if len(row) > 7 else 'NO'
                    )
                contador += 1
            except Exception as e:
                errors.append(f"Error fila: {row} - {str(e)}")

        contexto = {
            'contador': contador,
            'errors': errors[:10],  # Mostrar solo primeros errores
        }
        return render(request, 'cds/importar_cds_result.html', contexto)

    return render(request, 'cds/importar_cds.html')

def cds_exportar_cds(request):
    """
            Exporta todos los CD's a un archivo CSV descargable
        """
    # Obtener todos los CD's (ordenados por título como en el modelo)
    cds = Cds.objects.all().order_by('titulo')

    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Cds.csv"'

    # Crear escritor CSV
    writer = csv.writer(response)

    # Escribir encabezados
    writer.writerow([
        'ID',
        'Título',
        'Grupo',
        'Año',
        'Copiado',
        'Falta',
        'Tipo',
        'Notas'
    ])

    # Escribir datos
    for cd in cds:
        writer.writerow([
            cd.id,
            cd.titulo,
            cd.grupo,
            cd.anyo,
            cd.copiado,
            cd.falta,
            cd.tipo,
            cd.notas
        ])

    return response


def cds_exportar_cds_xlsx(request):
    """
        Exporta todos los CDs DVDs o Bluray a Excel usando pandas
    """
    try:
        import pandas as pd

        # Convertir QuerySet a lista de diccionarios
        libros_data = list(Cds.objects.all().order_by('titulo').values(
            'id',
            'titulo',
            'grupo__grupo', # Relación ForeignKey
            'anyo',
            'copiado',
            'falta',
            'tipo__tipo',  # Relación ForeignKey
            'notas'
        ))

        # Renombrar columnas para que sean más legibles
        rename_map = {
            'grupo__grupo': 'Grupo',
            'tipo__tipo': 'Tipo'
        }

        df = pd.DataFrame(libros_data)
        df.rename(columns=rename_map, inplace=True)

        # Asegurar orden de columnas
        columns_order = ['id', 'Título', 'Grupo', 'Año', 'Copiado', 'Falta', 'Tipo', 'Notas']
        df.columns = ['id', 'Título', 'Grupo', 'Año', 'Copiado', 'Falta', 'Tipo', 'Notas']

        # Ordenar por título
        df.sort_values(by='Título', inplace=True, ignore_index=True)

        # Crear respuesta HTTP
        filename = f'cds_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Escribir a Excel con formato
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='CDs', index=False)

            # Aplicar estilo con openpyxl
            worksheet = writer.sheets['CDs']

            # Cabeceras en negrita y azul
            header_font = Font(bold=True, color='FFFFFF')
            header_fill = PatternFill(start_color='2196F3', end_color='2196F3', fill_type='solid')

            for col_num in range(1, len(df.columns) + 1):
                cell = worksheet.cell(row=1, column=col_num)
                cell.font = header_font
                cell.fill = header_fill

            # Ancho de columnas automático
            for col_num in range(1, len(df.columns) + 1):
                column = worksheet.column_dimensions[worksheet.cell(row=1, column=col_num).column_letter]
                longest = max(
                    (len(str(cell.value)) for cell in worksheet[col_num]),
                    default=len(df.columns[col_num - 1])
                )
                column.width = longest + 2

        return response

    except Exception as e:
        from django.contrib import messages
        messages.error(request, f'Error al exportar: {str(e)}')
        return redirect('cds:cds')


def cds_editar_cd(request, id):
    cd = get_object_or_404(Cds, id=id)

    if request.method == 'POST':
        formulario = CdsForm(request.POST, instance=cd)
        if formulario.is_valid():
            formulario.save()
            return redirect('cds:cds')
    else:
        formulario = CdsForm(instance=cd)

    contexto = {
        'formulario': formulario,
        'libro': cd,
    }
    return render(request, 'cds/editar_cd.html', contexto)

def cds_borrar_cd(request, id):
    cd = get_object_or_404(Cds, id=id)

    if request.method == 'POST':
        cd.delete()
        return redirect('cds:cds')

    contexto = {
        'cd': cd,
    }
    return render(request, 'cds/borrar_cd.html', contexto)

