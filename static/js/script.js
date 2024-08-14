// Ventana de mensajes flash globales
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay mensajes flash en la página
    var flashMessages = document.querySelector('.flashconfig');

    if (flashMessages) {
        // Mostrar los mensajes flash si existen
        flashMessages.style.display = 'block';

        // Ocultar el mensaje después de 3 segundos
        setTimeout(function() {
            flashMessages.style.display = 'none';
        }, 3000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay mensajes flash en la página
    var flashMessages = document.querySelector('.flashes');

    if (flashMessages) {
        // Mostrar los mensajes flash si existen
        flashMessages.style.display = 'block';

        // Ocultar el mensaje después de 3 segundos
        setTimeout(function() {
            flashMessages.style.display = 'none';
        }, 3000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay mensajes flash en la página
    var flashMessages = document.querySelector('.flashusers');

    if (flashMessages) {
        // Mostrar los mensajes flash si existen
        flashMessages.style.display = 'block';

        // Ocultar el mensaje después de 3 segundos
        setTimeout(function() {
            flashMessages.style.display = 'none';
        }, 3000);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay mensajes flash en la página
    var flashMessages = document.querySelector('.flashglo');

    if (flashMessages) {
        // Mostrar los mensajes flash si existen
        flashMessages.style.display = 'block';

        // Ocultar el mensaje después de 3 segundos
        setTimeout(function() {
            flashMessages.style.display = 'none';
        }, 3000);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay mensajes flash en la página
    var flashMessages = document.querySelector('.flashbase');
    
    if (flashMessages) {
        // Mostrar los mensajes flash si existen
        flashMessages.style.display = 'block';

        // Ocultar el mensaje después de 3 segundos (10000 milisegundos)
        setTimeout(function() {
            flashMessages.style.display = 'none';
        }, 3000);
    }
});

    //Ventana de Login - olvidar contraseña
    function Passwordremember() {
        // Obtener el elemento del mensaje de flash
        var flashMessage = document.getElementById('flashmessage-login');
        
        // Mostrar el mensaje de flash
        flashMessage.style.display = 'block';
        
        // Ocultar el mensaje después de 3 segundos (10000 milisegundos)
        setTimeout(function() {
            flashMessage.style.display = 'none';
        }, 3000);
    }

//cambio de imagen en la interfaz del logo del establecimiento
document.addEventListener('DOMContentLoaded', function() {
    // Manejo de cambio de imagen del logo solo interfaz
    const fileInput = document.getElementById('logo');
    const image = document.querySelector('.imagen');

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function(e) {
                image.src = e.target.result;
            };

            reader.readAsDataURL(file);
        }
    });
});
//Icono de politicas del establecimiento
document.addEventListener('DOMContentLoaded', function() {
    var input = document.getElementById('politicas-file');
    var filenameDisplay = document.getElementById('politicas-filename');
    var image = document.getElementById('politicas-img');

    // Mostrar el campo de archivo cuando se hace clic en la imagen
    image.addEventListener('click', function() {
        input.click();
    });

    // Cuando el usuario selecciona un archivo, actualizar el texto con el nombre del archivo
    input.addEventListener('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            filenameDisplay.textContent = file.name; // Muestra el nombre del archivo
        } else {
            filenameDisplay.textContent = 'No hay archivo seleccionado';
        }
    });
});

//Actualización de imagen de banner
document.addEventListener('DOMContentLoaded', function() {
    var input = document.getElementById('imagen-banner');
    var preview = document.getElementById('banner-preview');

    input.addEventListener('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            // Revertir a la imagen original si no se selecciona un archivo
            preview.src = "{{ url_for('static', filename='uploads/' + (config.imagen_banner if config.imagen_banner else 'default-banner.png')) }}";
        }
    });
});


///Actualización de cartas de recomendación
$(document).ready(function() {
    $('#cartas_reco').change(function(event) {
        // Obtén el archivo del input
        var file = this.files[0];

        // Verifica si hay un archivo seleccionado
        if (file) {
            var reader = new FileReader();

            // Define qué hacer cuando el archivo se cargue
            reader.onload = function(event) {
                // Actualiza la fuente de la imagen con el resultado del FileReader
                $('#cartas_reco_preview').attr('src', event.target.result);
            };

            // Lee el archivo como una URL de datos
            reader.readAsDataURL(file);
        } else {
            // Si no hay archivo, podrías establecer una imagen predeterminada o manejar el caso de error
            $('#cartas_reco_preview').attr('src', 'assets/Documents-SWCPHK/CartasRecomendacion/default-recommendation.jpeg');
        }
    });
});

//Cambio de imagen de profile
function previewProfileImage(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
        document.getElementById('profileImage').src = e.target.result;
    }
    
    if (file) {
        reader.readAsDataURL(file);
    }
}


///Imagen de de configuracion de interfaz
document.addEventListener('DOMContentLoaded', function() {
    var input = document.getElementById('imagen-banner');
    var preview = document.getElementById('banner-preview');

    input.addEventListener('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            // Revertir a la imagen original si no se selecciona un archivo
            preview.src = "{{ url_for('static', filename='uploads/' + (config.imagen_banner if config.imagen_banner else 'default-banner.png')) }}";
        }
    });
});

//Actiulizacion de foto de usuarios
document.addEventListener('DOMContentLoaded', function() {
    const fotoUsuarioInput = document.getElementById('foto_usuario');
    const fotoUsuarioPreview = document.getElementById('foto_usuario_preview');

    if (fotoUsuarioInput && fotoUsuarioPreview) {
        fotoUsuarioInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            const reader = new FileReader();

            if (file) {
                reader.onload = function(e) {
                    fotoUsuarioPreview.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    } else {
        console.error('Elemento(s) con ID "foto_usuario" o "foto_usuario_preview" no encontrado(s).');
    }
});    

$(document).ready(function() {
    // Función para obtener la fecha actual en formato YYYY-MM-DD
    function obtenerFechaActual() {
        const ahora = new Date();
        const opciones = { year: 'numeric', month: '2-digit', day: '2-digit' };
        return ahora.toLocaleDateString(undefined, opciones).replace(/\//g, '-');
    }

    // Mostrar ventana de Sueldos pagados
    const sueldoDataElement = $('#sueldo-data');
    const sueldoCalculado = parseFloat(sueldoDataElement.attr('data-sueldo-calculado'));

    if (sueldoCalculado !== 0) {
        $('#popup-sueldo').show();
    }

    function mostrarMensaje(mensaje, tipo) {
        const container = $('#message-container');
        container.text(mensaje);
        container.removeClass('success error'); // Elimina clases anteriores
        container.addClass(tipo); // Agrega la clase para el tipo de mensaje
        container.show();
                
        setTimeout(function() {
            container.fadeOut();
        }, 5000); // Oculta el mensaje después de 5 segundos
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

    // Manejar clic en el botón de guardar en el popup de sueldo
    $('#acceptButton-s').click(function() {
        // Obtener los datos necesarios
        const sueldoCalculado = parseFloat($('#sueldo-data').attr('data-sueldo-calculado'));
        const idUsuario = $('#form-consulta input[name="id_usuario"]').val();
        const fechaActual = obtenerFechaActual(); // Obtener la fecha en formato YYYY-MM-DD

        // Obtener la hora actual en formato HH:MM:SS
        const ahora = new Date();
        const horaActual = ahora.toTimeString().split(' ')[0]; // Extrae la parte de la hora en formato HH:MM:SS
    
        // Enviar datos al servidor
        fetch('/guardar_pago', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fecha_pago: fechaActual,
                hora_pago: horaActual, // Enviar la hora en formato HH:MM:SS
                monto_total_pago: sueldoCalculado,
                id_usuariofok: idUsuario
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarMensaje('Pago guardado exitosamente', 'success');
                // Ocultar el popup y limpiar datos
                $('#popup-sueldo').hide();
                $('#form-consulta input[type="text"]').val('');
                $('#form-consulta input[type="date"]').val('');
                $('#tabla-datos tbody').empty();
            } else {
                mostrarMensaje('Error al guardar el pago: ' + data.error, 'error');
            }
        })
        .catch(error => mostrarMensaje('Error: ' + error, 'error'));
    });

    // Manejar clic en el botón de guardar y generar PDF en el popup de sueldo
    $('#pdfButton-s').click(function() {
        // Obtener los datos necesarios
        const sueldoCalculado = parseFloat($('#sueldo-data').attr('data-sueldo-calculado'));
        const idUsuario = $('#form-consulta input[name="id_usuario"]').val();
        const fechaActual = obtenerFechaActual(); // Fecha actual en formato YYYY-MM-DD

        // Recopilar datos de la tabla
        const tablaDatos = [];
        $('#tabla-datos tbody tr').each(function() {
            const row = $(this);
            const idUsuario = row.find('td').eq(0).text();
            const usuario = row.find('td').eq(1).text();
            const fecha = row.find('td').eq(2).text();
            const horaEntrada = row.find('td').eq(3).text();
            const horaSalida = row.find('td').eq(4).text();
            tablaDatos.push({ idUsuario, usuario, fecha, horaEntrada, horaSalida });
        });

        // Enviar datos al servidor
        fetch('/guardar_y_generar_pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fecha_pago: fechaActual,
                monto_total_pago: sueldoCalculado,
                id_usuariofok: idUsuario,
                registros: tablaDatos
            })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sueldo.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url); // Limpiar la URL del blob

            // Ocultar el popup y limpiar el formulario
            $('#popup-sueldo').hide();
            $('#form-consulta input[type="text"]').val('');
            $('#form-consulta input[type="date"]').val('');
            $('#tabla-datos tbody').empty();
        })
        .catch(error => {
            console.error('Error al generar el PDF:', error);
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Mostrar ventana emergente
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
                // Asegúrate de que esta línea se esté ejecutando
            } else {
                console.error('Error al guardar la hora:', data.error);
                // Puedes agregar aquí una notificación de error para el usuario
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Puedes agregar aquí una notificación de error para el usuario
        });
    });

    // Cierra la ventana emergente al hacer clic en el botón "Cancelar"
    cancelButton.addEventListener('click', function() {
        popup.style.display = 'none'; // Cierra la ventana emergente
    });
});

// Crea ventana emergente para Usuario existente
$(".alert").fadeIn();

setTimeout(function() {
    $(".alert").fadeOut();
}, 5000); // 5 seconds
