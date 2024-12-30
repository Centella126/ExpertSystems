<?php
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

// Consultar la última temperatura deseada registrada
$sql = "SELECT temperatura_deseada FROM registros ORDER BY hora DESC LIMIT 1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Si hay registros, tomamos la última temperatura registrada
    $row = $result->fetch_assoc();
    echo json_encode(['temperatura' => $row['temperatura_deseada']]);
} else {
    // Si no hay registros, devolver una temperatura por defecto
    echo json_encode(['temperatura' => 37]); // Temperatura por defecto
}

$conn->close();
?>
