<?php
// Habilitar la visualización de errores para depuración
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Conectar a la base de datos
$host = 'localhost';
$user = 'root';
$password = 'qwerty123';
$dbname = 'Registros_Diarios';

$conn = new mysqli($host, $user, $password, $dbname);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Obtener el estado de la incubadora y la temperatura deseada
$estado = isset($_GET['estado']) ? $_GET['estado'] : '';
$temperatura_deseada = isset($_GET['temperatura']) ? $_GET['temperatura'] : null;

// Si no se proporciona temperatura deseada, obtenemos la última registrada
if ($temperatura_deseada === null) {
    // Consultar la última temperatura deseada registrada
    $sql = "SELECT temperatura_deseada FROM registros ORDER BY hora DESC LIMIT 1";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // Si hay registros, tomamos la última temperatura registrada
        $row = $result->fetch_assoc();
        $temperatura_deseada = $row['temperatura_deseada'];
    } else {
        // Si no hay registros previos, asignamos un valor por defecto
        $temperatura_deseada = 37; // Temperatura por defecto
    }
}

// Generar la temperatura real aleatoria basada en la temperatura deseada
// La diferencia de la temperatura real puede ser de -1 a +1°C respecto a la deseada
$temperatura_real = $temperatura_deseada + rand(-1, 1);

// Generar temperatura exterior aleatoria entre 20°C y 30°C
$temperatura_exterior = rand(20, 30);

// Obtener el día actual (como número de día en el mes)
$dia = date('j'); // Día del mes (1-31)

// Establecer la fecha y hora actual
$fecha = date('Y-m-d');
$hora = date('H:i:s');

// Si el estado de la incubadora es 'Abrir' o 'Cerrar', lo registramos
if ($estado) {
    // Insertar el registro con la acción de abrir o cerrar la incubadora
    $sql = "INSERT INTO registros (fecha, hora, temperatura_deseada, temperatura_real, temperatura_exterior, estado_incubadora, dia)
            VALUES (?, ?, ?, ?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssdddsd", $fecha, $hora, $temperatura_deseada, $temperatura_real, $temperatura_exterior, $estado, $dia);

    if ($stmt->execute()) {
        echo json_encode(['mensaje' => 'Acción realizada correctamente', 'estado' => $estado]);
    } else {
        echo json_encode(['error' => 'Error al actualizar el estado.']);
    }

    $stmt->close();
} else {
    // Si no se proporcionó un estado, simplemente actualizamos la temperatura sin cambiar el estado
    // Aquí actualizamos la temperatura deseada para el último registro del día
    $sql = "UPDATE registros SET temperatura_deseada = ?, temperatura_real = ?, temperatura_exterior = ? 
            WHERE dia = ? ORDER BY hora DESC LIMIT 1";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("dddi", $temperatura_deseada, $temperatura_real, $temperatura_exterior, $dia);

    if ($stmt->execute()) {
        echo json_encode(['mensaje' => 'Temperatura deseada actualizada correctamente.']);
    } else {
        echo json_encode(['error' => 'Error al actualizar la temperatura.']);
    }

    $stmt->close();
}

// Cerrar la conexión
$conn->close();
?>
