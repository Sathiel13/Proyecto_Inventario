import sys
import sqlite3
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QVBoxLayout, QFormLayout, QLineEdit, \
    QComboBox, QLabel, QDateEdit, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QDate


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Renta de Mobiliario")
        self.setGeometry(100, 100, 600, 400)

        # Crear botones para cada opción
        btn_agregar_cliente = QPushButton("Agregar Cliente", self)
        btn_agregar_cliente.clicked.connect(self.mostrar_ventana_agregar_cliente)

        btn_agregar_producto = QPushButton("Agregar Producto", self)
        btn_agregar_producto.clicked.connect(self.mostrar_ventana_agregar_producto)

        btn_agregar_renta = QPushButton("Agregar Renta", self)
        btn_agregar_renta.clicked.connect(self.mostrar_ventana_agregar_renta)

        btn_mostrar_clientes = QPushButton("Mostrar Clientes", self)
        btn_mostrar_clientes.clicked.connect(self.mostrar_clientes)

        btn_mostrar_productos = QPushButton("Mostrar Productos", self)
        btn_mostrar_productos.clicked.connect(self.mostrar_productos)

        btn_mostrar_rentas = QPushButton("Mostrar Rentas", self)
        btn_mostrar_rentas.clicked.connect(self.mostrar_rentas)

        #Creo el boton de editar
        btn_editar = QPushButton("Editar", self)  # Crear el botón "Editar"
        btn_editar.setObjectName("btnEditar")  # Asignar un ID al botón
        btn_editar.clicked.connect(self.editar)  # Conectar el botón a la función editar

        # Crear layout y añadir los botones
        layout = QVBoxLayout()
        layout.addWidget(btn_agregar_cliente)
        layout.addWidget(btn_agregar_producto)
        layout.addWidget(btn_agregar_renta)
        layout.addWidget(btn_mostrar_clientes)
        layout.addWidget(btn_mostrar_productos)
        layout.addWidget(btn_mostrar_rentas)
        layout.addWidget(btn_editar)  # Agregar el botón "Editar" al layout

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def editar(self):
        # Abrir la ventana de edición
        self.ventana_editar = VentanaEditar()
        self.ventana_editar.show()


    def mostrar_ventana_agregar_cliente(self):
        self.ventana_cliente = VentanaAgregarCliente()
        self.ventana_cliente.show()

    def mostrar_ventana_agregar_producto(self):
        self.ventana_producto = VentanaAgregarProducto()
        self.ventana_producto.show()

    def mostrar_ventana_agregar_renta(self):
        self.ventana_renta = VentanaAgregarRenta()
        self.ventana_renta.show()

    def mostrar_clientes(self):
        self.ventana_clientes = VentanaMostrarClientes()
        self.ventana_clientes.show()

    def mostrar_productos(self):
        self.ventana_productos = VentanaMostrarProductos()
        self.ventana_productos.show()

    def mostrar_rentas(self):
        self.ventana_rentas = VentanaMostrarRentas()
        self.ventana_rentas.show()

class VentanaEditar(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Información")
        self.setGeometry(150, 150, 400, 300)

        # Crear widgets
        self.label_seleccion = QLabel("¿Qué deseas editar?")
        self.combo_opciones = QComboBox()
        self.combo_opciones.addItems(["Cliente", "Producto"])  # Opciones para editar

        self.label_id = QLabel("ID del elemento a editar:")
        self.input_id = QLineEdit()

        self.label_nuevo_valor = QLabel("Nuevo valor:")
        self.input_nuevo_valor = QLineEdit()

        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.guardar_cambios)

        # Crear layout e insertar widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label_seleccion)
        layout.addWidget(self.combo_opciones)
        layout.addWidget(self.label_id)
        layout.addWidget(self.input_id)
        layout.addWidget(self.label_nuevo_valor)
        layout.addWidget(self.input_nuevo_valor)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_cambios(self):
        # Obtener los valores ingresados por el usuario
        id_elemento = self.input_id.text()
        nuevo_valor = self.input_nuevo_valor.text()

        # Validar que los campos no estén vacíos
        if not id_elemento or not nuevo_valor:
            QMessageBox.warning(self, "Advertencia", "Todos los campos deben estar llenos.")
            return

        # Aquí defines la lógica para actualizar el elemento
        # Por ejemplo, podrías buscar el elemento en una lista o base de datos y actualizarlo
        # Para este ejemplo, solo imprimimos un mensaje de confirmación
        print(f"Actualizando el elemento con ID {id_elemento} al nuevo valor: {nuevo_valor}")
        QMessageBox.information(self, "Éxito", f"Elemento con ID {id_elemento} actualizado correctamente.")

        # Cerrar la ventana de edición
        self.close()

class VentanaAgregarCliente(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar Cliente")
        self.setGeometry(200, 200, 400, 300)

        layout = QFormLayout()

        self.nombre_input = QLineEdit(self)
        layout.addRow("Nombre del Cliente", self.nombre_input)

        self.telefono_input = QLineEdit(self)
        layout.addRow("Teléfono", self.telefono_input)

        self.direccion_input = QLineEdit(self)
        layout.addRow("Dirección", self.direccion_input)

        btn_guardar_cliente = QPushButton("Guardar Cliente", self)
        btn_guardar_cliente.clicked.connect(self.guardar_cliente)
        layout.addWidget(btn_guardar_cliente)

        self.setLayout(layout)

    def guardar_cliente(self):
        nombre_cliente = self.nombre_input.text()
        telefono_cliente = self.telefono_input.text()
        direccion_cliente = self.direccion_input.text()

        if nombre_cliente and telefono_cliente and direccion_cliente:
            if self.guardar_en_bd_cliente(nombre_cliente, telefono_cliente, direccion_cliente):
                self.close()
            else:
                print("Error al guardar el cliente.")
        else:
            print("Todos los campos deben ser completados.")

    def guardar_en_bd_cliente(self, nombre_cliente, telefono_cliente, direccion_cliente):
        try:
            db_path = os.path.abspath("database/renta_mobiliario.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO clientes (nombre, telefono, direccion) VALUES (?, ?, ?)",
                           (nombre_cliente, telefono_cliente, direccion_cliente))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar cliente en la base de datos: {e}")
            return False


class VentanaAgregarProducto(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar Producto")
        self.setGeometry(200, 200, 400, 300)

        layout = QFormLayout()

        self.nombre_input = QLineEdit(self)
        layout.addRow("Nombre del Producto", self.nombre_input)

        self.precio_input = QLineEdit(self)
        layout.addRow("Precio de Renta", self.precio_input)

        self.cantidad_input = QLineEdit(self)
        layout.addRow("Cantidad", self.cantidad_input)

        btn_guardar_producto = QPushButton("Guardar Producto", self)
        btn_guardar_producto.clicked.connect(self.guardar_producto)
        layout.addWidget(btn_guardar_producto)

        self.setLayout(layout)

    def guardar_producto(self):
        nombre_producto = self.nombre_input.text()
        precio_producto = self.precio_input.text()
        cantidad_producto = self.cantidad_input.text()

        if nombre_producto and precio_producto and cantidad_producto:
            try:
                precio_producto = float(precio_producto)
                cantidad_producto = int(cantidad_producto)
                if self.guardar_en_bd_producto(nombre_producto, precio_producto, cantidad_producto):
                    self.close()
                else:
                    print("Error al guardar el producto.")
            except ValueError:
                print("El precio debe ser un número válido y la cantidad un entero.")
        else:
            print("Todos los campos deben ser completados.")

    def guardar_en_bd_producto(self, nombre_producto, precio_producto, cantidad_producto):
        try:
            db_path = os.path.abspath("database/renta_mobiliario.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO productos (nombre, precio_renta, cantidad) VALUES (?, ?, ?)",
                           (nombre_producto, precio_producto, cantidad_producto))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar producto en la base de datos: {e}")
            return False


class VentanaAgregarRenta(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar Renta")
        self.setGeometry(200, 200, 400, 300)

        layout = QFormLayout()

        # ComboBox para seleccionar el cliente
        self.cliente_combo = QComboBox(self)
        self.cargar_clientes()
        layout.addRow("Selecciona Cliente", self.cliente_combo)

        # ComboBox para seleccionar el producto
        self.producto_combo = QComboBox(self)
        self.cargar_productos()
        layout.addRow("Selecciona Producto", self.producto_combo)

        # Campo para cantidad
        self.cantidad_input = QLineEdit(self)
        self.cantidad_input.setPlaceholderText("Cantidad de productos")
        self.cantidad_input.textChanged.connect(self.calcular_total)
        layout.addRow("Cantidad", self.cantidad_input)

        # Campos para fechas con QDateEdit
        self.fecha_inicio_input = QDateEdit(self)
        self.fecha_inicio_input.setDate(QDate.currentDate())  # Establecer fecha actual como predeterminada
        self.fecha_inicio_input.setDisplayFormat("yyyy-MM-dd")  # Formato de fecha
        layout.addRow("Fecha Inicio", self.fecha_inicio_input)

        self.fecha_fin_input = QDateEdit(self)
        self.fecha_fin_input.setDate(QDate.currentDate())  # Establecer fecha actual como predeterminada
        self.fecha_fin_input.setDisplayFormat("yyyy-MM-dd")  # Formato de fecha
        layout.addRow("Fecha Fin", self.fecha_fin_input)

        self.precio_total_input = QLineEdit(self)
        self.precio_total_input.setReadOnly(True)
        layout.addRow("Precio Total", self.precio_total_input)

        btn_guardar_renta = QPushButton("Guardar Renta", self)
        btn_guardar_renta.clicked.connect(self.guardar_renta)
        layout.addWidget(btn_guardar_renta)

        self.setLayout(layout)

    def cargar_clientes(self):
        try:
            db_path = os.path.abspath("database/renta_mobiliario.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT id, nombre FROM clientes")
            clientes = cursor.fetchall()

            for cliente in clientes:
                self.cliente_combo.addItem(cliente[1], cliente[0])  # nombre, id del cliente

            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar clientes: {e}")

    def cargar_productos(self):
        try:
            db_path = os.path.abspath("database/renta_mobiliario.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT id, nombre, precio_renta FROM productos")
            productos = cursor.fetchall()

            for producto in productos:
                self.producto_combo.addItem(producto[1], (producto[0], producto[2]))  # nombre, id y precio del producto

            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar productos: {e}")

    def calcular_total(self):
        producto_id, precio_producto = self.producto_combo.currentData()
        cantidad = self.cantidad_input.text()

        if cantidad and precio_producto:
            try:
                cantidad = int(cantidad)
                total = cantidad * precio_producto
                self.precio_total_input.setText(f"${total:.2f}")
            except ValueError:
                self.precio_total_input.setText("Error en la cantidad")
        else:
            self.precio_total_input.clear()

    def guardar_renta(self):
        cliente_id = self.cliente_combo.currentData()
        producto_id, _ = self.producto_combo.currentData()
        fecha_inicio = self.fecha_inicio_input.date().toString("yyyy-MM-dd")
        fecha_fin = self.fecha_fin_input.date().toString("yyyy-MM-dd")
        precio_total = self.precio_total_input.text()

        if fecha_inicio > fecha_fin:
            print("La fecha de inicio no puede ser mayor que la fecha de fin.")
            return

        if cliente_id and producto_id and fecha_inicio and fecha_fin and precio_total:
            try:
                precio_total = float(precio_total.replace('$', ''))
                if self.guardar_en_bd_renta(cliente_id, producto_id, fecha_inicio, fecha_fin, precio_total):
                    self.close()
                else:
                    print("Error al guardar la renta.")
            except ValueError:
                print("El precio total debe ser un número válido.")
        else:
            print("Todos los campos deben ser completados.")

    def guardar_en_bd_renta(self, cliente_id, producto_id, fecha_inicio, fecha_fin, precio_total):
        try:
            db_path = os.path.abspath("database/renta_mobiliario.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO rentas (cliente_id, producto_id, fecha_inicio, fecha_fin, precio_total) VALUES (?, ?, ?, ?, ?)",
                (cliente_id, producto_id, fecha_inicio, fecha_fin, precio_total))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar renta en la base de datos: {e}")
            return False


class VentanaMostrarClientes(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clientes")
        self.setGeometry(200, 200, 600, 400)

        # Crear tabla para mostrar los clientes
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)  # ID, Nombre, Teléfono
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono"])

        self.cargar_clientes()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def cargar_clientes(self):
        try:
            db_path = os.path.abspath("database/renta_mobiliario.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT id, nombre, telefono FROM clientes")
            clientes = cursor.fetchall()

            self.table.setRowCount(len(clientes))

            for i, cliente in enumerate(clientes):
                for j, value in enumerate(cliente):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))

            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar los clientes: {e}")


class VentanaMostrarProductos(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Productos")
        self.setGeometry(200, 200, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # ID, Nombre, Precio, Cantidad
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Cantidad"])

        self.cargar_productos()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def cargar_productos(self):
        try:
            db_path = os.path.abspath("database/renta_mobiliario.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT id, nombre, precio_renta, cantidad FROM productos")
            productos = cursor.fetchall()

            self.table.setRowCount(len(productos))

            for i, producto in enumerate(productos):
                for j, value in enumerate(producto):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))

            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar los productos: {e}")


class VentanaMostrarRentas(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rentas")
        self.setGeometry(200, 200, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)  # ID, Cliente, Producto, Fecha Inicio, Fecha Fin, Precio Total
        self.table.setHorizontalHeaderLabels(["ID", "Cliente", "Producto", "Fecha Inicio", "Fecha Fin", "Precio Total"])

        self.cargar_rentas()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def cargar_rentas(self):
        try:
            db_path = os.path.abspath("database/renta_mobiliario.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT rentas.id, clientes.nombre, productos.nombre, rentas.fecha_inicio, rentas.fecha_fin, rentas.precio_total "
                "FROM rentas "
                "JOIN clientes ON rentas.cliente_id = clientes.id "
                "JOIN productos ON rentas.producto_id = productos.id")
            rentas = cursor.fetchall()

            self.table.setRowCount(len(rentas))

            for i, renta in enumerate(rentas):
                for j, value in enumerate(renta):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))

            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar las rentas: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Cargar el archivo QSS
    try:
        with open("ui/Estilos.css", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Archivo de estilos 'styles.css' no encontrado.")
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
