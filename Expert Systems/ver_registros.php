<?php
// Conectar a la base de datos
$host = 'localhost';
$user = 'root';
$password = 'qwerty123';
$dbname = 'Registros_Reales';

$conn = new mysqli($host, $user, $password, $dbname);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Inicializamos los arreglos para las temperaturas
$temperatura_deseada = [];
$temperatura_real = [];
$temperatura_exterior = [];
$hora_registros = [];
$estado_incubadora = [];

// Verificamos si se ha enviado el parámetro de día
if (isset($_GET['dia'])) {
    $dia = $_GET['dia'];

    // Consulta para obtener los registros del día seleccionado
    $sql = "SELECT hora, temperatura_deseada, temperatura_real, temperatura_exterior, estado_incubadora FROM registros WHERE dia = ? ORDER BY hora ASC";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $dia); // Vinculamos el parámetro del día a la consulta

    if ($stmt->execute()) {
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            // Guardamos los resultados en los arreglos
            while ($row = $result->fetch_assoc()) {
                $hora_registros[] = $row['hora'];
                $temperatura_deseada[] = $row['temperatura_deseada'];
                $temperatura_real[] = $row['temperatura_real'];
                $temperatura_exterior[] = $row['temperatura_exterior'];
                $estado_incubadora[] = $row['estado_incubadora']; // Guardamos el estado de la incubadora
            }
        } else {
            echo "<p>No se encontraron registros para el Día $dia.</p>";
        }
    } else {
        echo "Error en la consulta: " . $stmt->error;
    }

    $stmt->close();
} else {
    echo "<p>Por favor, seleccione un día para ver los registros.</p>";
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registros del Día</title>
    <link rel="stylesheet" href="stylescanva.css"> <!-- Estilos para la tabla y gráficas -->
</head>
<body>

<h2>Registros del Día <?php echo $dia; ?></h2>

<!-- Tabla de registros -->
<table border="1" cellspacing="0" cellpadding="10">
    <thead>
        <tr>
            <th>Hora</th>
            <th>Temperatura Deseada (°C)</th>
            <th>Temperatura Real (°C)</th>
            <th>Temperatura Exterior (°C)</th>
            <th>Estado de la Incubadora</th> <!-- Nueva columna para el estado -->
        </tr>
    </thead>
    <tbody>
        <?php
        // Imprimir los registros en una tabla
        foreach ($hora_registros as $index => $hora) {
            echo "<tr>";
            echo "<td>" . $hora . "</td>";
            echo "<td>" . $temperatura_deseada[$index] . "</td>";
            echo "<td>" . $temperatura_real[$index] . "</td>";
            echo "<td>" . $temperatura_exterior[$index] . "</td>";
            echo "<td>" . $estado_incubadora[$index] . "</td>"; // Imprimir el estado de la incubadora
            echo "</tr>";
        }
        ?>
    </tbody>
</table>

<!-- Gráficas de las temperaturas -->
<canvas id="graficaTemperatura1"></canvas> <!-- Gráfico 1: Temperatura deseada vs real -->
<canvas id="graficaTemperatura2"></canvas> <!-- Gráfico 2: Temperatura real vs exterior -->

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script> <!-- Librería para las gráficas -->
<script>
    const ctx1 = document.getElementById('graficaTemperatura1').getContext('2d');
    const ctx2 = document.getElementById('graficaTemperatura2').getContext('2d');

    const graficaTemperatura1 = new Chart(ctx1, {
        type: 'line',
        data: {
            labels: <?php echo json_encode($hora_registros); ?>,
            datasets: [{
                label: 'Temperatura Deseada (°C)',
                data: <?php echo json_encode($temperatura_deseada); ?>,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: false
            }, {
                label: 'Temperatura Real (°C)',
                data: <?php echo json_encode($temperatura_real); ?>,
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: false
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 1500, // Animación más suave
                easing: 'easeInOutQuad'
            }
        }
    });

    const graficaTemperatura2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: <?php echo json_encode($hora_registros); ?>,
            datasets: [{
                label: 'Temperatura Real (°C)',
                data: <?php echo json_encode($temperatura_real); ?>,
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: false
            }, {
                label: 'Temperatura Exterior (°C)',
                data: <?php echo json_encode($temperatura_exterior); ?>,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: false
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 1500, // Animación más suave
                easing: 'easeInOutQuad'
            }
        }
    });
</script>

</body>
</html>
