import csv

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl.styles import Font, PatternFill

from .forms import AplicacionesForm
from .models import Aplicaciones, Origen


# Create your views here.
def aplicaciones_listar(request):
    aplicaciones = Aplicaciones.objects.all()
    return render(request, 'aplicaciones/aplicaciones_listar.html', {'aplicaciones': aplicaciones, })

def aplicaciones_alta_aplicacion(request):
    if request.method == 'POST':
        formulario = AplicacionesForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('aplicaciones:aplicaciones')
    else:
        formulario = AplicacionesForm()

    contexto = {
        'formulario': formulario,
    }
    return render(request, 'aplicaciones/editar_aplicacion.html', contexto)

def aplicaciones_buscar_aplicacion(request):
    resultado = None

    if request.method == 'GET':
        aplicacion = request.GET.get('aplicacion', '').strip()

        if aplicacion:
            query = Q()

            query &= Q(aplicacion__icontains=aplicacion)

            resultado = Aplicaciones.objects.filter(query)

    contexto = {
        'resultado': resultado,
        'aplicacion_buscar': request.GET.get('aplicacion', ''),
    }
    return render(request, 'aplicaciones/buscar_aplicaciones.html', contexto)

def aplicaciones_importar_aplicaciones(request):
    """
        Importa aplicaciones desde un archivo CSV
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
                origen = Origen.objects.filter(origen=row[2]).first()
                Aplicaciones.objects.create(
                    aplicacion=row[1],
                    origen=origen,
                    instalar=row[3],
                    favoritos=row[4],
                    notas=row[5] if len(row) > 5 else 'NO'
                )
                contador += 1
            except Exception as e:
                errors.append(f"Error fila: {row} - {str(e)}")

        contexto = {
            'contador': contador,
            'errors': errors[:10],  # Mostrar solo primeros errores
        }
        return render(request, 'aplicaciones/importar_aplicaciones_result.html', contexto)

    return render(request, 'aplicaciones/importar_aplicaciones.html')

def aplicaciones_exportar_aplicaciones(request):
    """
        Exporta todas las aplicaciones a un archivo CSV descargable
    """
    # Obtener todas las Aplicaciones (ordenados por aplicacion como en el modelo)
    aplicaciones = Aplicaciones.objects.all().order_by('aplicacion')

    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Aplicaciones.csv"'

    # Crear escritor CSV
    writer = csv.writer(response)

    # Escribir encabezados
    writer.writerow([
        'ID',
        'Aplicacion',
        'Origen',
        'Instalar',
        'Favoritos',
        'Notas',
    ])

    # Escribir datos
    for aplicacion in aplicaciones:
        writer.writerow([
            aplicacion.id,
            aplicacion.aplicacion,
            aplicacion.origen,
            aplicacion.instalar,
            aplicacion.favoritos,
            aplicacion.notas
        ])

    return response

def aplicaciones_exportar_aplicaciones_xlsx(request):
    """
        Exporta todas las Aplicaciones
    """
    try:
        import pandas as pd

        # Convertir QuerySet a lista de diccionarios
        aplicaciones_data = list(Aplicaciones.objects.all().order_by('aplicacion').values(
            'id',
            'aplicacion',
            'origen__origen',  # Relación ForeignKey
            'instalar',
            'favoritos',
            'notas',
        ))

        # Renombrar columnas para que sean más legibles
        rename_map = {
            'origen_origen': 'Origen',
        }

        df = pd.DataFrame(aplicaciones_data)
        df.rename(columns=rename_map, inplace=True)

        # Asegurar orden de columnas
        columns_order = ['id', 'Aplicacion', 'Origen', 'Instalar', 'Copiado', 'Notas']
        df.columns = ['id', 'Aplicacion', 'Origen', 'Instalar', 'Copiado', 'Notas']

        # Ordenar por título
        df.sort_values(by='Aplicacion', inplace=True, ignore_index=True)

        # Crear respuesta HTTP
        filename = f'aplicaciones_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Escribir a Excel con formato
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Aplicaciones', index=False)

            # Aplicar estilo con openpyxl
            worksheet = writer.sheets['Aplicaciones']

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
        return redirect('aplicaciones:aplicaciones')

def aplicaciones_editar_aplicacion(request, id):
    aplicacion = get_object_or_404(Aplicaciones, id=id)

    if request.method == 'POST':
        formulario = AplicacionesForm(request.POST, instance=aplicacion)
        if formulario.is_valid():
            formulario.save()
            return redirect('aplicaciones:aplicaciones')
    else:
        formulario = AplicacionesForm(instance=aplicacion)

    contexto = {
        'formulario': formulario,
        'aplicacion': aplicacion,
    }
    return render(request, 'aplicaciones/editar_aplicacion.html', contexto)


def aplicaciones_borrar_aplicacion(request, id):
    aplicacion = get_object_or_404(Aplicaciones, id=id)

    if request.method == 'POST':
        aplicacion.delete()
        return redirect('aplicaciones:aplicaciones')

    contexto = {
        'aplicacion': aplicacion,
    }
    return render(request, 'aplicaciones/borrar_aplicacion.html', contexto)