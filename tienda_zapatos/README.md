# Sistema de Inventario de Zapatos — SQLAlchemy ORM

## 1. Información del proyecto

| Información | Descripción |
|---|---|
| Estudiante | [Joel David Berdugo] |
| Asignatura | [DESARROLLO DE APLICACIONES CON ACCESO A DATOS] |
| Docente | [Eduardo Pimienta] |
| Fecha | [17/11/2026] |
| Lenguaje de programación | Python |
| ORM utilizado | SQLAlchemy |
| Base de datos | SQLite |

## 2. Descripción del proyecto

### ¿En qué consiste el programa?

Este programa permite administrar el inventario de una pequeña tienda de zapatos desde la consola. El usuario puede registrar zapatos con su modelo, talla y precio; consultar todos los productos registrados; buscar un zapato por su identificador; actualizar el precio de un producto y eliminarlo cuando ya no sea necesario.

Los datos se guardan de forma permanente en una base de datos SQLite llamada `zapateria.db`. El programa utiliza SQLAlchemy como ORM, lo que permite trabajar con objetos Python en lugar de escribir consultas SQL directamente.

### ¿Qué funcionalidades tiene?

El sistema permite realizar las siguientes operaciones:

- Registrar zapatos.
- Consultar el inventario.
- Buscar zapatos por ID.
- Actualizar precios.
- Eliminar zapatos.
- Conservar los datos después de cerrar y volver a ejecutar la aplicación.

## 3. Estructura del proyecto

```text
tienda_zapatos/
├── main.py
├── datos.py
├── requirements.txt
├── README.md
└── evidencias/
```

### Explicación de los archivos

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Contiene el menú principal y la interacción con el usuario. Solicita los datos, valida algunas entradas y llama a las funciones del archivo `datos.py`. |
| `datos.py` | Contiene la configuración de SQLAlchemy, el modelo `Zapato`, la conexión con SQLite y las funciones CRUD. |
| `requirements.txt` | Contiene la dependencia necesaria para ejecutar el proyecto, en este caso SQLAlchemy. |
| `zapateria.db` | Es el archivo de base de datos SQLite. Se genera automáticamente la primera vez que se ejecuta `main.py`. |

## 4. Instalación y ejecución

### Paso 1. Requisitos

- Tener instalado Python 3.
- Tener instalado `pip`.
- Contar con SQLAlchemy 2.0 o superior.

### Paso 2. Instalación de dependencias

Ejecuta el siguiente comando en la terminal, dentro de la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
```

### Paso 3. Ejecución

Ejecuta el programa con el siguiente comando:

```bash
python main.py
```

### Paso 4. Resultado esperado

Al ejecutar correctamente la aplicación, se muestra el siguiente menú:

```text
===== TIENDA DE ZAPATOS =====
1. Registrar zapato
2. Listar zapatos
3. Buscar zapato por ID
4. Actualizar precio
5. Eliminar zapato
6. Salir
Seleccione una opción:
```

La primera vez que se ejecuta, también se crea automáticamente el archivo `zapateria.db` y la tabla `zapatos`.

## 5. Documentación técnica — Preguntas obligatorias

### Pregunta 1. Modelo y tabla

**¿Qué clase de Python representa la tabla de la base de datos? Explica cómo SQLAlchemy identifica el nombre de la tabla y sus columnas.**

**Respuesta:**

La clase Python que representa la tabla de la base de datos es `Zapato`. Esta clase hereda de `Base`, la cual fue creada utilizando `DeclarativeBase`. SQLAlchemy utiliza esta clase para crear y administrar la tabla `zapatos` en la base de datos SQLite.

El nombre de la tabla se define mediante el atributo:

```python
__tablename__ = "zapatos"
```

Las columnas se identifican mediante los atributos de la clase declarados con `Mapped` y `mapped_column`. Por ejemplo, `id` es la clave primaria y se genera automáticamente; `modelo` es un texto; `talla` es un número entero; y `precio` es un número real.

**Fragmento de código relacionado:**

```python
class Zapato(Base):
    __tablename__ = "zapatos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    modelo: Mapped[str] = mapped_column(String(100))
    talla: Mapped[int] = mapped_column()
    precio: Mapped[float] = mapped_column()
```

En este código, SQLAlchemy interpreta que la clase `Zapato` representa la tabla `zapatos`. Cada atributo corresponde a una columna de la tabla. El atributo `id` se configura como clave primaria y autoincremental, por lo que la base de datos genera automáticamente un número único para cada zapato registrado.

### Pregunta 2. Creación de la base de datos

**¿Qué ocurre cuando ejecutas el programa por primera vez? Explica cómo se crea la base de datos `zapateria.db` y la tabla `zapatos`.**

**Respuesta:**

Cuando se ejecuta el programa por primera vez, la función `main()` llama a `datos.inicializar_bd()`. Esta función utiliza `Base.metadata.create_all(engine)` para crear las tablas definidas en los modelos de SQLAlchemy.

La conexión se configura con:

```python
engine = create_engine("sqlite:///zapateria.db", echo=False)
```

Si el archivo `zapateria.db` no existe, SQLAlchemy lo crea automáticamente. Después, se crea la tabla `zapatos` con las columnas `id`, `modelo`, `talla` y `precio`.

Si el archivo y la tabla ya existen, el programa no los borra ni los recrea; simplemente verifica que existan y continúa utilizando los datos almacenados.

**Fragmento de código relacionado:**

```python
engine = create_engine("sqlite:///zapateria.db", echo=False)

def inicializar_bd():
    Base.metadata.create_all(engine)
```

### Pregunta 3. Registro de zapatos

**Cuando seleccionas la opción de registrar un zapato, ¿qué recorrido siguen los datos desde el menú hasta quedar almacenados en SQLite? Identifica las funciones utilizadas.**

**Respuesta:**

Cuando el usuario selecciona la opción `1`, el programa solicita el modelo, la talla y el precio del zapato. Luego valida que el modelo no esté vacío, que la talla sea mayor que cero y que el precio sea mayor que cero.

Después, `main.py` llama a la función `datos.crear_zapato(modelo, talla, precio)`. Dentro de esta función se crea un objeto de la clase `Zapato` con los datos ingresados. Luego se abre una sesión con `Session(engine)`, se agrega el objeto con `session.add(zapato)` y se guarda permanentemente en la base de datos con `session.commit()`.

El recorrido de los datos es el siguiente:

1. El usuario ingresa los datos en `main.py`.
2. El programa valida los valores.
3. Se llama a `datos.crear_zapato()`.
4. Se crea un objeto `Zapato`.
5. Se abre una sesión de SQLAlchemy.
6. Se agrega el objeto con `session.add()`.
7. Se confirma la transacción con `session.commit()`.
8. Los datos quedan almacenados en la tabla `zapatos` del archivo `zapateria.db`.

**Fragmento de código relacionado:**

```python
def crear_zapato(modelo, talla, precio):
    zapato = Zapato(
        modelo=modelo,
        talla=talla,
        precio=precio
    )

    with Session(engine) as session:
        session.add(zapato)
        session.commit()

    return True
```

### Pregunta 4. Sesiones y transacciones

**¿Para qué se utiliza una sesión de SQLAlchemy? ¿Qué ocurriría si agregas o modificas un objeto, pero no confirmas la transacción con `commit()`?**

**Respuesta:**

Una sesión de SQLAlchemy sirve para administrar la comunicación entre la aplicación Python y la base de datos. Permite agregar, consultar, modificar y eliminar objetos, y luego guardar los cambios en la base de datos.

En este proyecto, la sesión se utiliza en todas las operaciones CRUD. Por ejemplo, al registrar un zapato se abre una sesión, se agrega el objeto y se confirma la transacción:

```python
with Session(engine) as session:
    session.add(zapato)
    session.commit()
```

Si se agrega o modifica un objeto pero no se ejecuta `session.commit()`, los cambios no se guardan permanentemente en la base de datos. Al cerrar la sesión, esos cambios se pierden. Por ejemplo, si se cambia el precio de un zapato con `zapato.precio = nuevo_precio`, pero no se llama a `session.commit()`, el precio seguirá siendo el anterior cuando se vuelva a consultar la base de datos.

### Pregunta 5. Búsqueda por ID

**¿Cómo funciona la búsqueda de zapatos por ID? Explica qué devuelve tu función cuando encuentra el registro y qué devuelve cuando no existe.**

**Respuesta:**

La búsqueda por ID se realiza en la función `buscar_zapato(id_zapato)`. Esta función recibe el identificador ingresado por el usuario y utiliza `session.get(Zapato, id_zapato)` para buscar un registro con ese ID en la tabla `zapatos`.

Si encuentra el zapato, la función devuelve el objeto `Zapato` correspondiente. En `main.py`, ese objeto se utiliza para mostrar el ID, el modelo, la talla y el precio del producto.

Si no existe un zapato con ese ID, la función devuelve `None`. En `main.py`, el programa compara el resultado con `None` y muestra el mensaje “Zapato no encontrado.”

**Fragmento de código relacionado:**

```python
def buscar_zapato(id_zapato):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)

    if zapato is None:
        return None

    return zapato
```

### Pregunta 6. Actualización de precios

**¿Cómo se actualiza el precio de un zapato mediante el ORM? Explica cómo se obtiene el objeto, cómo se modifica su atributo y cómo se guarda el cambio.**

**Respuesta:**

Para actualizar el precio, el programa solicita el ID del zapato y el nuevo precio. Luego llama a la función `datos.actualizar_precio(id_zapato, nuevo_precio)`.

Dentro de la función, se abre una sesión y se busca el zapato con `session.get(Zapato, id_zapato)`. Si el objeto existe, se modifica directamente su atributo `precio`. Después, se guarda el cambio en la base de datos con `session.commit()`.

Si el ID no existe, la función devuelve `False` y el programa muestra “Zapato no encontrado.”

**Fragmento de código relacionado:**

```python
def actualizar_precio(id_zapato, nuevo_precio):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)

        if zapato is None:
            return False

        zapato.precio = nuevo_precio
        session.commit()

        return True
```

### Pregunta 7. Eliminación de registros

**¿Qué ocurre cuando eliminas un zapato? Explica cómo compruebas que el registro ya no existe en la base de datos.**

**Respuesta:**

Cuando se elimina un zapato, el programa solicita su ID y llama a la función `datos.eliminar_zapato(id_zapato)`. La función busca el objeto con `session.get(Zapato, id_zapato)`.

Si el zapato existe, se elimina utilizando `session.delete(zapato)` y se confirma la eliminación con `session.commit()`. Después de esto, el registro desaparece de la tabla `zapatos`.

Para comprobar que el registro ya no existe, se puede seleccionar la opción `2` para listar todos los zapatos. El zapato eliminado ya no debe aparecer. También se puede usar la opción `3` para buscar el ID eliminado; el programa debe mostrar “Zapato no encontrado.”

**Fragmento de código relacionado:**

```python
def eliminar_zapato(id_zapato):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)

        if zapato is None:
            return False

        session.delete(zapato)
        session.commit()

        return True
```

### Pregunta 8. Persistencia de datos

**¿Qué sucede con los zapatos registrados cuando cierras y vuelves a ejecutar el programa? Explica por qué permanecen almacenados.**

**Respuesta:**

Cuando se cierra el programa y se vuelve a ejecutar, los zapatos que no fueron eliminados siguen apareciendo en el listado. Esto ocurre porque los datos no se guardan solamente en la memoria del programa, sino en el archivo de base de datos `zapateria.db`.

La persistencia se logra porque cada operación de registro, actualización o eliminación utiliza `session.commit()`. Este método confirma la transacción y guarda los cambios de forma permanente en SQLite.

Para comprobarlo, se registraron zapatos, se cerró el programa con la opción `6` y se volvió a ejecutar con `python main.py`. Al seleccionar la opción `2`, los registros que no fueron eliminados seguían disponibles.

## 6. Pruebas de funcionamiento y evidencias

### Prueba 1. Registrar zapatos

**Acción realizada:** registrar dos zapatos.

**Datos utilizados:**

- Zapato 1: Modelo `Nike Air`, talla `40`, precio `150000`.
- Zapato 2: Modelo `Adidas Running`, talla `42`, precio `180000`.

**Resultado obtenido:** el programa mostró el mensaje “Zapato registrado correctamente.” para cada uno de los dos zapatos.

**Evidencia:**

```text
===== TIENDA DE ZAPATOS =====
1. Registrar zapato
2. Listar zapatos
3. Buscar zapato por ID
4. Actualizar precio
5. Eliminar zapato
6. Salir
Seleccione una opción: 1
Modelo: Nike Air
Talla: 40
Precio: 150000
Zapato registrado correctamente.

Seleccione una opción: 1
Modelo: Adidas Running
Talla: 42
Precio: 180000
Zapato registrado correctamente.
```

**Archivo de evidencia:** `evidencias/prueba_1_registrar_zapatos.png`

### Prueba 2. Listar inventario

**Acción realizada:** consultar todos los zapatos registrados.

**Resultado obtenido:** el programa mostró los dos zapatos registrados, incluyendo su ID generado automáticamente, modelo, talla y precio.

**Evidencia:**

```text
Seleccione una opción: 2
ID: 1 | Modelo: Nike Air | Talla: 40 | Precio: $150000.00
ID: 2 | Modelo: Adidas Running | Talla: 42 | Precio: $180000.00
```

**Archivo de evidencia:** `evidencias/prueba_2_listar_zapatos.png`

### Prueba 3. Buscar por ID

**ID utilizado:** `1`

**Resultado obtenido:** el programa encontró el zapato con ID 1 y mostró sus datos completos.

**Evidencia:**

```text
Seleccione una opción: 3
ID del zapato: 1
ID: 1 | Modelo: Nike Air | Talla: 40 | Precio: $150000.00
```

**Archivo de evidencia:** `evidencias/prueba_3_buscar_zapato.png`

### Prueba 4. Actualizar precio

**Zapato seleccionado:** ID `1`, modelo `Nike Air`.

**Precio anterior:** `150000`.

**Precio nuevo:** `165000`.

**Resultado obtenido:** el programa mostró “Precio actualizado.” Al consultar nuevamente el zapato, se comprobó que el precio cambió de `$150000.00` a `$165000.00`.

**Evidencia:**

```text
Seleccione una opción: 4
ID del zapato: 1
Nuevo precio: 165000
Precio actualizado.

Seleccione una opción: 3
ID del zapato: 1
ID: 1 | Modelo: Nike Air | Talla: 40 | Precio: $165000.00
```

**Archivo de evidencia:** `evidencias/prueba_4_actualizar_precio.png`

### Prueba 5. Eliminar zapato

**ID eliminado:** `2`

**Resultado obtenido:** el programa mostró “Zapato eliminado.” Al listar nuevamente los zapatos, el registro con ID 2 ya no aparecía.

**Evidencia:**

```text
Seleccione una opción: 5
ID del zapato: 2
Zapato eliminado.

Seleccione una opción: 2
ID: 1 | Modelo: Nike Air | Talla: 40 | Precio: $165000.00
```

**Archivo de evidencia:** `evidencias/prueba_5_eliminar_zapato.png`

### Prueba 6. Comprobar persistencia

**Acción realizada:** cerrar el programa con la opción `6` y ejecutarlo nuevamente con `python main.py`.

**Resultado obtenido:** el zapato con ID 1 seguía registrado después de cerrar y volver a abrir la aplicación. Esto demuestra que los datos se almacenan permanentemente en `zapateria.db`.

**Evidencia:**

```text
===== TIENDA DE ZAPATOS =====
1. Registrar zapato
2. Listar zapatos
3. Buscar zapato por ID
4. Actualizar precio
5. Eliminar zapato
6. Salir
Seleccione una opción: 2
ID: 1 | Modelo: Nike Air | Talla: 40 | Precio: $165000.00
```

**Archivo de evidencia:** `evidencias/prueba_6_persistencia_datos.png`

### Pruebas con registros inexistentes

| Operación | ¿Qué sucedió? |
|---|---|
| Buscar ID inexistente | El programa mostró el mensaje “Zapato no encontrado.” porque la función `buscar_zapato()` devolvió `None`. |
| Actualizar ID inexistente | El programa mostró el mensaje “Zapato no encontrado.” porque la función `actualizar_precio()` devolvió `False`. |
| Eliminar ID inexistente | El programa mostró el mensaje “Zapato no encontrado.” porque la función `eliminar_zapato()` devolvió `False`. |

## 7. Conclusiones

Al implementar las operaciones CRUD utilizando SQLAlchemy, aprendí a conectar una aplicación Python con una base de datos SQLite y a guardar información de forma permanente. También comprendí cómo funcionan los modelos, las sesiones y las transacciones dentro de un ORM.

La principal diferencia entre trabajar con objetos Python y escribir sentencias SQL directamente es que, con SQLAlchemy, se utilizan clases y objetos. Por ejemplo, en lugar de escribir una consulta SQL como `INSERT INTO zapatos`, se crea un objeto `Zapato` y se agrega a una sesión con `session.add()`. Esto hace que el código sea más organizado y fácil de mantener.

La principal dificultad fue comprender cómo SQLAlchemy administra las sesiones y las transacciones. La solución fue utilizar `with Session(engine) as session` en cada operación y llamar a `session.commit()` después de agregar, modificar o eliminar un registro. Así se garantiza que los cambios queden guardados permanentemente en la base de datos.