<?php
// Conectar a la base de datos
$host = 'localhost';
$user = 'root';
$password = 'qwerty123';
$dbname = 'Registros_Diarios';

// Crear conexión
$conn = new mysqli($host, $user, $password);

// Verificar conexión
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Crear base de datos si no existe
$sql = "CREATE DATABASE IF NOT EXISTS $dbname";
if ($conn->query($sql) === TRUE) {
    echo "Base de datos '$dbname' creada o ya existe.<br>";
} else {
    echo "Error al crear base de datos: " . $conn->error . "<br>";
}

// Seleccionar la base de datos
$conn->select_db($dbname);

// Crear tabla si no existe
$sql = "CREATE TABLE IF NOT EXISTS registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    hora TIME,
    temperatura_deseada FLOAT,
    temperatura_real FLOAT,
    temperatura_exterior FLOAT,
    estado_incubadora VARCHAR(10),
    dia INT
)";

if ($conn->query($sql) === TRUE) {
    echo "Tabla 'registros' creada o ya existe.<br>";
} else {
    echo "Error al crear tabla: " . $conn->error . "<br>";
}

// Función para generar temperaturas aleatorias
function generarTemperatura($min, $max) {
    return round(rand($min * 100, $max * 100) / 100, 2);  // Redondea a 2 decimales
}

// Función para generar el estado de la incubadora aleatorio (Abierto o Cerrado)
function generarEstadoIncubadora() {
    return rand(0, 1) ? 'Abierto' : 'Cerrado'; // Aleatorio entre "Abierto" y "Cerrado"
}

// Función para insertar un registro en la base de datos
function insertarRegistro($conn, $fecha, $hora, $temperatura_deseada, $temperatura_real, $temperatura_exterior, $estado_incubadora, $dia) {
    $stmt = $conn->prepare("INSERT INTO registros (fecha, hora, temperatura_deseada, temperatura_real, temperatura_exterior, estado_incubadora, dia)
                            VALUES (?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssdddsd", $fecha, $hora, $temperatura_deseada, $temperatura_real, $temperatura_exterior, $estado_incubadora, $dia);
    $stmt->execute();
    $stmt->close();
}

// Insertar datos aleatorios para los días 1 hasta 28
function insertarDatosAleatorios($conn) {
    for ($dia = 1; $dia <= 28; $dia++) {
        // Usar fecha dinámica para el día
        $fecha = date('Y-m-d', strtotime("+$dia day"));
        
        // Insertar datos cada hora para 24 horas
        for ($hora = 0; $hora < 24; $hora++) {
            // Generar hora en formato HH:00:00
            $hora_str = sprintf("%02d:00:00", $hora);
            
            // Generar temperaturas aleatorias
            $temp_deseada = generarTemperatura(36.0, 38.5);
            $temp_real = generarTemperatura(35.5, 38.0);
            $temp_exterior = generarTemperatura(15.0, 25.0);
            
            // Generar estado de la incubadora (Abierto o Cerrado)
            $estado_incubadora = generarEstadoIncubadora();
            
            // Insertar registro en la base de datos
            insertarRegistro($conn, $fecha, $hora_str, $temp_deseada, $temp_real, $temp_exterior, $estado_incubadora, $dia);
        }
    }
}

// Insertar datos para los días 1 hasta el 28
insertarDatosAleatorios($conn);

// Función para imprimir los registros de un día específico
function imprimirRegistros($conn, $dia) {
    $sql = "SELECT * FROM registros WHERE dia = $dia";
    $result = $conn->query($sql);
    
    if ($result->num_rows > 0) {
        echo "Registros del Día $dia:<br>";
        while($row = $result->fetch_assoc()) {
            echo "Fecha: " . $row["fecha"] . " | Hora: " . $row["hora"] . " | Temp. Deseada: " . $row["temperatura_deseada"] . "°C | Temp. Real: " . $row["temperatura_real"] . "°C | Temp. Exterior: " . $row["temperatura_exterior"] . "°C | Estado: " . $row["estado_incubadora"] . "<br>";
        }
    } else {
        echo "No se encontraron registros para el Día $dia.<br>";
    }
}

// Imprimir los registros para el Día 1 y Día 2
imprimirRegistros($conn, 1);
imprimirRegistros($conn, 2);

// Cerrar la conexión
$conn->close();
?>
