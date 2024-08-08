$(document).ready(function() {
    // Mostrar ventana de Sueldos pagados
    const sueldoDataElement = $('#sueldo-data');
    const sueldoCalculado = parseFloat(sueldoDataElement.attr('data-sueldo-calculado'));

    if (sueldoCalculado !== 0) {
        $('#popup-sueldo').show();
    }

    // Manejar clic en el botón de cancelar en el popup de sueldo
    $('#cancelButton-s').click(function() {
        // Limpiar los campos del formulario de consulta
        $('#form-consulta input[type="text"]').val('');
        $('#form-consulta input[type="date"]').val('');

        // Limpiar la tabla de datos
        $('#tabla-datos tbody').empty();

        // Ocultar el popup
        $('#popup-sueldo').hide();
    });

    // Funcionalidad para el botón de aceptar en el popup de sueldo
    $('#acceptButton-s').click(function() {
        $('#popup-sueldo').hide();
    });

    // Mostrar ventana de Trabajador y horas de turno
    var popup = document.getElementById('popup');
    var acceptButton = document.getElementById('acceptButton');
    var cancelButton = document.getElementById('cancelButton');

    // Muestra la ventana emergente
    popup.style.display = 'flex';

    // Función para actualizar la hora y los minutos en la ventana emergente
    function updateClock() {
        var now = new Date();
        var hour = String(now.getHours()).padStart(2, '0');
        var minute = String(now.getMinutes()).padStart(2, '0');
        document.getElementById('hour').textContent = hour;
        document.getElementById('minute').textContent = minute;
    }

    // Actualiza la hora y los minutos inmediatamente y luego cada segundo
    updateClock();
    setInterval(updateClock, 1000);

    // Verifica el ID del usuario desde el atributo `data-user-id`
    var userId = document.body.getAttribute('data-user-id');
    console.log('ID del usuario:', userId);

    // Cierra la ventana emergente y envía la hora al servidor al hacer clic en el botón de aceptar
    acceptButton.addEventListener('click', function() {
        console.log('Botón Aceptar clickeado'); // Línea de depuración

        // Obtiene la hora actual
        var now = new Date();
        var hour = String(now.getHours()).padStart(2, '0');
        var minute = String(now.getMinutes()).padStart(2, '0');
        var idUsuario = userId; // Obtener el ID del usuario desde el atributo `data-user-id`

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
        console.log('Botón Cancelar clickeado'); // Línea de depuración
        popup.style.display = 'none';
    });

    // Crea ventana emergente para Usuario existente
    $(".alert").fadeIn();

    setTimeout(function() {
        $(".alert").fadeOut();
    }, 5000); // 5 seconds

    // Cambia automáticamente la foto de perfil
    function previewImage(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        if (file) {
            reader.onload = function(e) {
                // Obtén el elemento de imagen y actualiza su src
                document.getElementById('profileImage').src = e.target.result;
            }
            // Lee el archivo como una URL de datos
            reader.readAsDataURL(file);
        }
    }

    // Cambia automáticamente la foto de cartas recomendación
    $('#foto_usuario').change(function(event) {
        var reader = new FileReader();
        reader.onload = function(event) {
            $('#foto_usuario_preview').attr('src', event.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    });

    $('#cartas_reco').change(function(event) {
        var reader = new FileReader();
        reader.onload = function(event) {
            $('#cartas_reco_preview').attr('src', event.target.result);
        }
        reader.readAsDataURL(this.files[0]);
    });

    // Login ventana
    function mostrarMensaje() {
        alert("Comuniquese con su administrador");
    }
});
