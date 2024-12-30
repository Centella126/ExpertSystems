<?php
if ((isset($_POST['accion']) && $_POST['accion'] === 'mover') || (isset($_GET['accion']) && $_GET['accion'] === 'mover')) {
    // Ejecutar el script Python
    $output = shell_exec('python3 gpioDBSERVOS.py 2>&1');

    if ($output === null) {
        // Hubo un error al ejecutar el script
        echo "Error: No se pudo mover el servo. Revisa el script Python.";
    } else {
        // Éxito en la ejecución
        echo "Servo movido correctamente.";
    }
    exit(); // Detener ejecución para evitar que se envíe contenido adicional
} else {
    // Respuesta para solicitudes inválidas
    echo "Acción inválida. Debes enviar una solicitud POST o GET con 'accion=mover'.";
    exit();
}
