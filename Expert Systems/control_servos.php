<?php
if (isset($_POST['accion'])) {
    $accion = $_POST['accion'];

    if ($accion === 'cerrar') {
        // Ejecutar el script Python para cerrar los servos
        shell_exec('python3 control_servos.py cerrar 2>&1');
    } elseif ($accion === 'abrir') {
        // Ejecutar el script Python para abrir los servos
        shell_exec('python3 control_servos.py abrir 2>&1');
    } else {
        echo "Acción inválida. Debes enviar 'cerrar' o 'abrir'.";
    }
} else {
    echo "Acción inválida. Debes enviar una solicitud POST con 'accion'.";
}
