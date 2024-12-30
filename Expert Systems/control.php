<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Control de Referencia</title>
</head>
<body>
    <h2>Ingresar Referencia para el Control</h2>
    <form method="POST" action="">
        <label for="referencia">Valor de Referencia:</label>
        <input type="number" step="0.01" id="referencia" name="referencia" required>
        <button type="submit">Ejecutar Control</button>
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Obtener el valor de referencia del formulario
        $referencia = floatval($_POST['referencia']);
        echo "<p>Ejecutando el script con referencia: $referencia</p>";

        // Ejecutar el script de Python
        $command = escapeshellcmd("python3 control.py $referencia");
        $output = shell_exec($command);

        // Mostrar salida del script (si hay)
        echo "<pre>$output</pre>";

        // Mostrar la gráfica si se generó
        if (file_exists("output.png")) {
            echo "<h3>Gráfica generada:</h3>";
            echo "<img src='output.png' alt='Gráfica de salida' style='width: 600px;'>";
        }
    }
    ?>
</body>
</html>
