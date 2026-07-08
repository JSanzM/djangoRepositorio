import csv

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from openpyxl.styles import Font, PatternFill

from .forms import LibroElectronicoForm
from .models import LibroElectronico


# Create your views here.
def libro_electronico_listar(request):
    libros = LibroElectronico.objects.all()
    return render(request, 'libro_electronico/libro_electronico.html', {'libros' : libros})

def libro_electronico_alta_libro(request):

    if request.method == 'POST':
        formulario = LibroElectronicoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('libro_electronico:libro_electronico')
    else:
        formulario = LibroElectronicoForm()

    contexto = {
        'formulario': formulario,
    }
    return render(request, 'libro_electronico/editar_libro_electronico.html', contexto)


def libro_electronico_buscar_libro(request):
    resultado = None

    if request.method == 'GET':
        autor = request.GET.get('autor', '').strip()
        titulo = request.GET.get('titulo', '').strip()

        if autor or titulo:
            query = Q()

            if autor:
                query &= Q(autor__icontains=autor)
            if titulo:
                query &= Q(titulo__icontains=titulo)

            resultado = LibroElectronico.objects.filter(query)

    contexto = {
        'resultado': resultado,
        'autor_buscar': request.GET.get('autor', ''),
        'titulo_buscar': request.GET.get('titulo', ''),
    }
    return render(request, 'libro_electronico/buscar_libro_electronico.html', contexto)

def libro_electronico_importar_libro(request):
    """
        Importa libros desde un archivo CSV
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
                if len(row) >= 4:
                    LibroElectronico.objects.create(
                        titulo=row[1],
                        autor=row[2],
                        serie=row[3],
                        bajado=row[4],
                        notas=row[5]
                    )
                    contador += 1
                else:
                    errors.append(f"Faltan campos: {row[1]}")
            except Exception as e:
                errors.append(f"Error fila: {row} - {str(e)}")

        contexto = {
            'contador': contador,
            'errors': errors[:10],  # Mostrar solo primeros errores
        }
        return render(request, 'libro_electronico/importar_libro_electronico_result.html', contexto)

    return render(request, 'libro_electronico/importar_libro_electronico.html')

def libro_electronico_exportar_libro(request):
    """
        Exporta todos los libros a un archivo CSV descargable
    """
    # Obtener todos los libros (ordenados por título como en el modelo)
    libros = LibroElectronico.objects.all().order_by('titulo')

    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="libro_electronico.csv"'

    # Crear escritor CSV
    writer = csv.writer(response)

    # Escribir encabezados
    writer.writerow([
        'ID',
        'Título',
        'Autor',
        'Serie',
        'Bajado',
        'Notas'
    ])

    # Escribir datos
    for libro in libros:
        writer.writerow([
            libro.id,
            libro.titulo,
            libro.autor,
            libro.serie,
            libro.bajado,
            libro.notas
        ])

    return response


def libro_electronico_exportar_libro_xlsx(request):
    """
        Exporta todos los libros a Excel usando pandas
        """
    try:
        import pandas as pd

        # Convertir QuerySet a lista de diccionarios
        libros_data = list(LibroElectronico.objects.all().order_by('titulo').values(
            'id',
            'titulo',
            'autor',
            'serie',
            'bajado',
            'notas'
        ))

        # Renombrar columnas para que sean más legibles
        df = pd.DataFrame(libros_data)

        # Asegurar orden de columnas
        columns_order = ['id', 'Título', 'Autor', 'Serie', 'Bajado', 'Notas']
        df.columns = ['id', 'Título', 'Autor', 'Serie', 'Bajado', 'Notas']

        # Ordenar por título
        df.sort_values(by='Título', inplace=True, ignore_index=True)

        # Crear respuesta HTTP
        filename = f'libros_electronicos{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Escribir a Excel con formato
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Libros', index=False)

            # Aplicar estilo con openpyxl
            worksheet = writer.sheets['Libros']

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
        return redirect('libro_electronico:libro_electronico')


def libro_electronico_editar_libro(request, id):
    libro = get_object_or_404(LibroElectronico, id=id)

    if request.method == 'POST':
        formulario = LibroElectronicoForm(request.POST, instance=libro)
        if formulario.is_valid():
            formulario.save()
            return redirect('libro_electronico:libro_electronico')
    else:
        formulario = LibroElectronicoForm(instance=libro)

    contexto = {
        'formulario': formulario,
        'libro': libro,
    }
    return render(request, 'libro_electronico/editar_libro_electronico.html', contexto)


def libro_electronico_borrar_libro(request, id):
    libro = get_object_or_404(LibroElectronico, id=id)

    if request.method == 'POST':
        libro.delete()
        return redirect('libro_electronico:libro_electronico')

    contexto = {
        'libro': libro,
    }
    return render(request, 'libro_electronico/borrar_libro_electronico.html', contexto)
