import csv

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl.styles import Font, PatternFill

from aplicaciones.models import Origen
from .forms import JuegosForm
from .models import Juegos, TipoJuego


# Create your views here.
def juegos_listar(request):
    juegos = Juegos.objects.all()
    return render(request, 'juegos/juegos_listar.html', {'juegos': juegos, })

def juegos_alta_juego(request):
    if request.method == 'POST':
        formulario = JuegosForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('juegos:juegos')
    else:
        formulario = JuegosForm()

    contexto = {
        'formulario': formulario,
    }
    return render(request, 'juegos/editar_juego.html', contexto)

def juegos_buscar_juego(request):
    resultado = None

    if request.method == 'GET':
        juego = request.GET.get('juego', '').strip()

        if juego:
            query = Q()

            query &= Q(nombre__icontains=juego)

            resultado = Juegos.objects.filter(query)

    contexto = {
        'resultado': resultado,
        'juego_buscar': request.GET.get('juego', ''),
    }
    return render(request, 'juegos/buscar_juegos.html', contexto)

def juegos_importar_juegos(request):
    """
        Importa Juegos  desde un archivo CSV
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
                origen = Origen.objects.filter(origen=row[4]).first()
                tipoJuego = TipoJuego.objects.filter(tipoJuego=row[2]).first()
                Juegos.objects.create(
                    nombre=row[1],
                    tipoJuego=tipoJuego,
                    instalar=row[3],
                    origen=origen,
                    notas=row[5] if len(row) > 5 else 'NO'
                )
                contador += 1
            except Exception as e:
                errors.append(f"Error fila: {row} - {str(e)}")

        contexto = {
            'contador': contador,
            'errors': errors[:10],  # Mostrar solo primeros errores
        }
        return render(request, 'juegos/importar_juegos_result.html', contexto)

    return render(request, 'juegos/importar_juegos.html')

def juegos_exportar_juegos(request):
    """
        Exporta todos los juegos a un archivo CSV descargable
    """
    # Obtener todos los juegos (ordenados por nombre como en el modelo)
    juegos = Juegos.objects.all().order_by('nombre')

    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Juegos.csv"'

    # Crear escritor CSV
    writer = csv.writer(response)

    # Escribir encabezados
    writer.writerow([
        'ID',
        'Nombre',
        'Tipo',
        'Instalar',
        'Origen',
        'Notas',
    ])

    # Escribir datos
    for juego in juegos:
        writer.writerow([
            juego.id,
            juego.nombre,
            juego.tipoJuego,
            juego.instalar,
            juego.origen,
            juego.notas
        ])

    return response

def juegos_exportar_juegos_xlsx(request):
    """
        Exporta todos los Juegos
    """
    try:
        import pandas as pd

        # Convertir QuerySet a lista de diccionarios
        juegos_data = list(Juegos.objects.all().order_by('nombre').values(
            'id',
            'nombre',
            'tipoJuego__tipoJuego',  # Relación ForeignKey
            'instalar',
            'origen',
            'notas',
        ))

        # Renombrar columnas para que sean más legibles
        rename_map = {
            'tipoJuego__tipoJuego': 'Tipo',
            'origen_origen': 'Origen',
        }

        df = pd.DataFrame(juegos_data)
        df.rename(columns=rename_map, inplace=True)

        # Asegurar orden de columnas
        columns_order = ['id', 'Nombre', 'Tipo', 'Instalar', 'Origen', 'Notas']
        df.columns = ['id', 'Nombre', 'Tipo', 'Instalar', 'Origen', 'Notas']

        # Ordenar por título
        df.sort_values(by='Nombre', inplace=True, ignore_index=True)

        # Crear respuesta HTTP
        filename = f'Juegos_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Escribir a Excel con formato
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Juegos', index=False)

            # Aplicar estilo con openpyxl
            worksheet = writer.sheets['Juegos']

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
        return redirect('juegos:juegos')

def juegos_editar_juego(request, id):
    juego = get_object_or_404(Juegos, id=id)

    if request.method == 'POST':
        formulario = JuegosForm(request.POST, instance=juego)
        if formulario.is_valid():
            formulario.save()
            return redirect('juegos:juegos')
    else:
        formulario = JuegosForm(instance=juego)

    contexto = {
        'formulario': formulario,
        'juego': juego,
    }
    return render(request, 'juegos/editar_juego.html', contexto)

def juegos_borrar_juego(request, id):
    juego = get_object_or_404(Juegos, id=id)

    if request.method == 'POST':
        juego.delete()
        return redirect('juegos:juegos')

    contexto = {
        'juego': juego,
    }
    return render(request, 'juegos/borrar_juego.html', contexto)

