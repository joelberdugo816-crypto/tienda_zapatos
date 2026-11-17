from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session
)


# =====================================
# 1. CONFIGURAR LA CONEXIÓN
# =====================================

engine = create_engine("sqlite:///zapateria.db", echo=False)


# =====================================
# 2. CREAR LA CLASE BASE
# =====================================

class Base(DeclarativeBase):
    pass


# =====================================
# 3. CREAR EL MODELO ZAPATO
# =====================================

class Zapato(Base):
    __tablename__ = "zapatos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    modelo: Mapped[str] = mapped_column(String(100))
    talla: Mapped[int] = mapped_column()
    precio: Mapped[float] = mapped_column()


# =====================================
# 4. CREAR LA TABLA
# =====================================

def inicializar_bd():
    Base.metadata.create_all(engine)


# =====================================
# 5. REGISTRAR ZAPATO
# =====================================

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


# =====================================
# 6. LISTAR ZAPATOS
# =====================================

def listar_zapatos():
    with Session(engine) as session:
        consulta = select(Zapato).order_by(Zapato.id)
        zapatos = session.scalars(consulta).all()

    return zapatos


# =====================================
# 7. BUSCAR POR ID
# =====================================

def buscar_zapato(id_zapato):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)

    return zapato


# =====================================
# 8. ACTUALIZAR PRECIO
# =====================================

def actualizar_precio(id_zapato, nuevo_precio):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)

        if zapato is None:
            return False

        zapato.precio = nuevo_precio
        session.commit()

    return True


# =====================================
# 9. ELIMINAR ZAPATO
# =====================================

def eliminar_zapato(id_zapato):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)

        if zapato is None:
            return False

        session.delete(zapato)
        session.commit()

    return True