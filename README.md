# SearchAI — AI Assistant for Systematic Literature Reviews

Interfaz gráfica (solo UI, sin lógica) construida con **Python + CustomTkinter**,
con estética moderna tipo Notion / GitHub Desktop / Cursor, tema oscuro y
componentes reutilizables.

## Instalación

```bash
pip install -r requirements.txt
```

> En Linux puede que necesites instalar Tk del sistema: `sudo apt install python3-tk`

## Ejecución

```bash
python main.py
```

Se abrirá la ventana principal (1500x900).

## Estructura del proyecto

```
SearchAI/
├── main.py                     # Punto de entrada, ensambla la ventana completa
├── requirements.txt
├── styles/
│   └── theme.py                # Paleta de colores, tipografías, spacing, iconos
├── components/                 # Widgets reutilizables (sin lógica de negocio)
│   ├── buttons.py               # PrimaryButton, SecondaryButton, OutlineButton, DangerButton, IconButton
│   ├── card.py                  # Card (contenedor de sección) y SectionLabel
│   ├── kpi_card.py               # Tarjeta de métrica (KPI)
│   ├── sidebar.py                # Navegación lateral (250px)
│   ├── header.py                  # Encabezado superior con selector de modelo IA
│   ├── editor.py                  # Editor de código estilo VSCode con resaltado básico
│   ├── table.py                   # Tabla reutilizable (ttk.Treeview estilizado)
│   └── console.py                 # Consola inferior estilo terminal
├── views/                       # Una vista = una sección del sidebar
│   ├── dashboard_view.py          # Sección 1: Research Context
│   ├── search_equation_view.py    # Sección 2: Search Equation
│   ├── dataset_view.py            # Sección 3: Dataset
│   ├── ai_analysis_view.py        # Sección 4: AI Analysis
│   ├── recommendations_view.py    # Sección 5: Recommendations
│   ├── history_view.py            # Sección 6: Iteration History
│   └── settings_view.py           # Configuración de modelo IA / API Key
└── assets/                      # Reservado para íconos/imágenes futuros
```

## Notas de arquitectura

- **Sin lógica de negocio**: todos los botones, tablas y campos están listos
  para conectarse a la lógica real (dataset, IA, guardado, etc.) pero
  actualmente solo muestran datos de ejemplo (placeholders) para representar
  el estado final de la interfaz.
- **Consola persistente**: el panel inferior (`components/console.py`) vive
  en `main.py` y expone un método `.append(mensaje, nivel)` listo para que el
  backend futuro reporte progreso (`"Loading dataset..."`, `"Search completed."`, etc.).
- **Navegación**: `main.py` instancia todas las vistas una sola vez y las
  apila con `tkraise()`, patrón clásico de "multi-page app" en Tkinter/CTk.
- **Theming centralizado**: cualquier cambio de color/tipografía se hace en
  `styles/theme.py` y se propaga a toda la app.
- **Tabla e ícono libres de dependencias externas**: los íconos son glifos
  Unicode (ver `Icon` en `theme.py`), por lo que no se requieren archivos de
  imagen para que la app funcione. Pueden reemplazarse por `CTkImage` desde
  `assets/` cuando se desee un set de íconos personalizado.

## Próximos pasos (fuera de este alcance)

- Conectar `Import CSV` / `Open Dataset` a lectura real de archivos.
- Conectar `Run Search`, `Validate` a la lógica de consulta.
- Conectar `AI Analysis` a un modelo real y actualizar KPIs/tabla dinámicamente.
- Persistir `Iteration History` y `Recommendations` en base de datos o archivo.
