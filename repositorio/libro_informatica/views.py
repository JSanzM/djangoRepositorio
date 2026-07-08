import csv

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from openpyxl.styles import Font, PatternFill

from .forms import LibroForm
from .models import LibroInformatica, Tipo, Subtipo


# Create your views here.
def libro_informatica_listar(request):
    libros = LibroInformatica.objects.all()
    return render(request, 'libro_informatica/libro_informatica.html',{'libros' : libros,})

def libro_informatica_alta_libro(request):

    if request.method == 'POST':
        formulario = LibroForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('libro_informatica:libro_informatica')
    else:
        formulario = LibroForm()

    contexto = {
        'formulario': formulario,
    }
    return render(request, 'libro_informatica/editar_libro.html', contexto)

def libro_informatica_buscar_libro(request):
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

            resultado = LibroInformatica.objects.filter(query)

    contexto = {
        'resultado': resultado,
        'autor_buscar': request.GET.get('autor', ''),
        'titulo_buscar': request.GET.get('titulo', ''),
    }
    return render(request, 'libro_informatica/buscar_libro.html', contexto)


def libro_informatica_importar_libro(request):
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
                    # Intentar obtener Tipo y Subtipo por nombre
                    tipo_obj = Tipo.objects.filter(tipo=row[5]).first()
                    subtipo_obj = Subtipo.objects.filter(subtipo=row[6]).first()

                    if tipo_obj and subtipo_obj:
                        LibroInformatica.objects.create(
                            titulo=row[1],
                            autor=row[2],
                            editorial=row[3],
                            anyo=int(row[4]),
                            tipo=tipo_obj,
                            subtipo=subtipo_obj,
                            leido=row[7] if len(row) > 7 else 'NO'
                        )
                        contador += 1
                    else:
                        errors.append(f"Falta Tipo o Subtipo: {row[1]}")
            except Exception as e:
                errors.append(f"Error fila: {row} - {str(e)}")

        contexto = {
            'contador': contador,
            'errors': errors[:10],  # Mostrar solo primeros errores
        }
        return render(request, 'libro_informatica/importar_libro_result.html', contexto)

    return render(request, 'libro_informatica/importar_libro.html')


def libro_informatica_exportar_libro(request):
    """
        Exporta todos los libros a un archivo CSV descargable
    """
    # Obtener todos los libros (ordenados por título como en el modelo)
    libros = LibroInformatica.objects.all().order_by('titulo')

    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="libro_informatica.csv"'

    # Crear escritor CSV
    writer = csv.writer(response)

    # Escribir encabezados
    writer.writerow([
        'ID',
        'Título',
        'Autor',
        'Editorial',
        'Año',
        'Tipo',
        'Subtipo',
        'Leído'
    ])

    # Escribir datos
    for libro in libros:
        writer.writerow([
            libro.id,
            libro.titulo,
            libro.autor,
            libro.editorial,
            libro.anyo,
            libro.tipo,
            libro.subtipo,
            libro.leido
        ])

    return response

def libro_informatica_exportar_libro_xlsx(request):
    """
        Exporta todos los libros a Excel usando pandas
        """
    try:
        import pandas as pd

        # Convertir QuerySet a lista de diccionarios
        libros_data = list(LibroInformatica.objects.all().order_by('titulo').values(
            'id',
            'titulo',
            'autor',
            'editorial',
            'anyo',
            'tipo__tipo',  # Relación ForeignKey
            'subtipo__subtipo',  # Relación ForeignKey
            'leido'
        ))

        # Renombrar columnas para que sean más legibles
        rename_map = {
            'tipo__tipo': 'Tipo',
            'subtipo__subtipo': 'Subtipo'
        }

        df = pd.DataFrame(libros_data)
        df.rename(columns=rename_map, inplace=True)

        # Asegurar orden de columnas
        columns_order = ['id', 'Título', 'Autor', 'Editorial', 'Año', 'Tipo', 'Subtipo', 'Leído']
        df.columns = ['id', 'Título', 'Autor', 'Editorial', 'Año', 'Tipo', 'Subtipo', 'Leído']

        # Ordenar por título
        df.sort_values(by='Título', inplace=True, ignore_index=True)

        # Crear respuesta HTTP
        filename = f'libros_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
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
        return redirect('libro_informatica:libro_informatica')

def libro_informatica_editar_libro(request, id):
    libro = get_object_or_404(LibroInformatica, id=id)

    if request.method == 'POST':
        formulario = LibroForm(request.POST, instance=libro)
        if formulario.is_valid():
            formulario.save()
            return redirect('libro_informatica:libro_informatica')
    else:
        formulario = LibroForm(instance=libro)

    contexto = {
        'formulario': formulario,
        'libro': libro,
    }
    return render(request, 'libro_informatica/editar_libro.html', contexto)

def libro_informatica_borrar_libro(request, id):
    libro = get_object_or_404(LibroInformatica, id=id)

    if request.method == 'POST':
        libro.delete()
        return redirect('libro_informatica:libro_informatica')

    contexto = {
        'libro': libro,
    }
    return render(request, 'libro_informatica/borrar_libro.html', contexto)
