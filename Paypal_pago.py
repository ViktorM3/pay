import paypalrestsdk
import logging
import webview

# Configuración de PayPal SDK (modo Sandbox)
paypalrestsdk.configure({
    "mode": "sandbox",  # Usa "sandbox" para pruebas
    "client_id": "AbVwaU_TK36s0E9b7jHCN58EgzGedjDJwPMAuIfBjtGUVmMmMX1xqtspdbcy9L1DhM1IWbKiTWQKpXIl",  # Sustituye con tu Client ID
    "client_secret": "EEscM1fDUfjo9KyhAnx1qkAtB1guf3-BvOxoCSCzz2fHM70uI4VDwwyd6XhQJBkKe5tFiDSaoP0tth6s"  # Sustituye con tu Client Secret
})


logging.basicConfig(level=logging.INFO)

class PuntoDeVenta:
    def __init__(self):
        self.total_compra = 0.0
    
    def agregar_producto(self, nombre, precio, cantidad):
        """Agrega productos a la compra y calcula el total."""
        self.total_compra += precio * cantidad
        print(f"{nombre} x{cantidad} agregado(s) - ${precio * cantidad:.2f}")
    
    def mostrar_total(self):
        """Muestra el total de la compra."""
        print(f"\nTotal a pagar: ${self.total_compra:.2f}")
    
    def procesar_pago_efectivo(self, monto_pago):
        """Simula el pago con efectivo."""
        if monto_pago >= self.total_compra:
            cambio = monto_pago - self.total_compra
            print(f"Pago aprobado. Cambio: ${cambio:.2f}")
        else:
            print("Pago insuficiente. Intenta nuevamente.")
    
    def crear_pago_paypal(self):
        """Crea un pago con PayPal y obtiene el enlace de redirección."""
        payment = paypalrestsdk.Payment({
            "intent": "sale",  # Tipo de pago
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": f"{self.total_compra:.2f}",  # Monto total
                    "currency": "USD"
                },
                "description": "Compra de ejemplo en Punto de Venta"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8080",  # Cambiar por la URL de retorno en la aplicación 
                "cancel_url": "http://localhost:8080"   # URL en caso de cancelación
            }
        })

        # Crear el pago
        if payment.create():
            print("Pago creado con éxito.")
            # Obtener el enlace de redirección
            for link in payment.links:
                if link.method == "REDIRECT":
                    print(f"Redirigir a: {link.href}")  # Mostrar el enlace de redirección de PayPal
                    return link.href
        else:
            print("Error al crear el pago:", payment.error)
            return None
    
    def procesar_pago(self):
        """Simula el proceso de pago basado en la elección del usuario."""
        print("\nOpciones de pago:")
        print("1. Pago en efectivo")
        print("2. Pago con PayPal")
        
        opcion_pago = input("\nSelecciona el método de pago (1 o 2): ").strip()

        if opcion_pago == "1":
            # Simular pago en efectivo
            monto_pago = float(input("Ingresa el monto a pagar con efectivo: $"))
            self.procesar_pago_efectivo(monto_pago)
        elif opcion_pago == "2":
            # Crear pago con PayPal y redirigir
            enlace_paypal = self.crear_pago_paypal()
            if enlace_paypal:
                print(f"Por favor, realiza el pago en PayPal visitando el siguiente enlace en la ventana: {enlace_paypal}")
                webview.create_window("pago Paypal" ,enlace_paypal)
                webview.start()
            else:
                print("Error al generar el enlace de pago con PayPal.")
        else:
            print("Opción no válida. Intenta nuevamente.")

    def finalizar_venta(self):
        """Simula la finalización de la venta."""
        print("\nVenta finalizada.")
        self.total_compra = 0.0  # Restablecer la compra para nueva venta



punto_de_venta = PuntoDeVenta()


punto_de_venta.agregar_producto("Café", 15.50, 2)
punto_de_venta.agregar_producto("Pan", 12.00, 1)
punto_de_venta.mostrar_total()


punto_de_venta.procesar_pago()

# Finalizar la venta
punto_de_venta.finalizar_venta()
