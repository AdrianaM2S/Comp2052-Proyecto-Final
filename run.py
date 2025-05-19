from app import create_app

# Crea la instancia de la aplicación Flask utilizando la factoría
app = create_app()

# Punto de entrada de la aplicación
if __name__ == '__main__':
    # Ejecuta el servidor Flask en modo desarrollo
    # host='0.0.0.0' permite que sea accesible desde otras máquinas en la red local
    # En producción, desactiva debug o usa un servidor como Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)