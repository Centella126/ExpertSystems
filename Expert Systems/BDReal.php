<?php
// Conectar a la base de datos
$host = 'localhost';
$user = 'root';
$password = 'qwerty123';
$dbname = 'Registros_Reales';

// Crear conexión
$conn = new mysqli($host, $user, $password);

// Verificar conexión
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Seleccionar la base de datos
$conn->select_db($dbname);

// Obtener los registros más recientes
$sql = "SELECT * FROM registros ORDER BY id DESC LIMIT 10"; // Obtiene los 10 registros más recientes
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<table border='1'><tr><th>ID</th><th>Fecha</th><th>Hora</th><th>Temperatura Real</th><th>Temperatura Exterior</th><th>Estado Incubadora</th><th>Día</th></tr>";
    while ($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["id"] . "</td><td>" . $row["fecha"] . "</td><td>" . $row["hora"] . "</td><td>" . $row["temperatura_real"] . "</td><td>" . $row["temperatura_exterior"] . "</td><td>" . $row["estado_incubadora"] . "</td><td>" . $row["dia"] . "</td></tr>";
    }
    echo "</table>";
} else {
    echo "No hay registros disponibles.";
}

$conn->close();
?>
