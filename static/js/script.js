document.addEventListener('DOMContentLoaded', function() {
    var popup = document.getElementById('popup');
    var acceptButton = document.getElementById('acceptButton');
    var cancelButton = document.getElementById('cancelButton');

    // Muestra la ventana emergente
    popup.style.display = 'flex';

    // Cierra la ventana emergente y envía la hora al servidor al hacer clic en el botón de aceptar
    acceptButton.addEventListener('click', function() {
        // Obtiene la hora actual
        var now = new Date();
        var hour = String(now.getHours()).padStart(2, '0');
        var minute = String(now.getMinutes()).padStart(2, '0');
        var idUsuario = 1; // Aquí deberías obtener el ID del usuario de alguna manera

        // Envía la hora al servidor
        fetch('/guardar_hora', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hora: hour, minuto: minute, id_usuario: idUsuario })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Hora guardada con éxito');
                popup.style.display = 'none'; // Cierra la ventana emergente
            } else {
                console.error('Error al guardar la hora:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Cierra la ventana emergente sin hacer nada al hacer clic en el botón de cancelar
    cancelButton.addEventListener('click', function() {
        popup.style.display = 'none';
    });

    // Actualiza la hora actual en la ventana emergente
    var now = new Date();
    var hour = String(now.getHours()).padStart(2, '0');
    var minute = String(now.getMinutes()).padStart(2, '0');
    document.getElementById('hour').textContent = hour;
    document.getElementById('minute').textContent = minute;
});


////Crea ventana vergente para Usuario existente

$(document).ready(function() {
    $(".alert").fadeIn();

    setTimeout(function() {
        $(".alert").fadeOut();
    }, 5000); // 5 seconds
});
