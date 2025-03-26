document.addEventListener("DOMContentLoaded", function() {
    var tipoCitaElement = document.getElementById('type');
    var doctorIdElement = document.getElementById('doc');
    var fechaElement = document.getElementById('fecha');
    var buttonAppointment = document.getElementById('appointment-button');

    var doctorsData = JSON.parse(document.getElementById('doctors-data').textContent);
    var appointmentsData = JSON.parse(document.getElementById('appointments-data').textContent);

    // Función para actualizar la visibilidad de los doctores
    function updateDoctorOptions(specialty) {
        for (var i = 0; i < doctorIdElement.options.length; i++) {
            var option = doctorIdElement.options[i];
            option.style.display = doctorsData[specialty]?.some(doctor => doctor.id == option.value) ? 'block' : 'none';
        }
    }

    // Inicializa el campo de doctores con la especialidad "General" por defecto
    updateDoctorOptions('General');

    tipoCitaElement.addEventListener('change', function(event) {
        var selectedType = event.target.value;

        // Actualiza la visibilidad de los doctores según la especialidad seleccionada
        updateDoctorOptions(selectedType);
    });

    fechaElement.addEventListener('change', function(event) {
        var selectedDoctor = doctorIdElement.value;
        var selectedFecha = new Date(event.target.value);
        var now = new Date(); // Fecha y hora actuales

        if (selectedDoctor && selectedFecha) {
            // Verificar si la fecha es en el pasado
            if (selectedFecha < now) {
                alert('No se pueden seleccionar fechas pasadas. Por favor, elige una fecha y hora futura.');
                fechaElement.value = '';  // Limpiar el campo de fecha
                buttonAppointment.disabled = true;
                return;
            }

            var isAvailable = checkAvailability(selectedDoctor, selectedFecha);

            if (!isAvailable) {
                alert('La fecha y hora seleccionadas ya están ocupadas para este doctor. Por favor, elige otra fecha u hora.');
                fechaElement.value = '';  // Limpiar el campo de fecha
                buttonAppointment.disabled = true;
            } else {
                buttonAppointment.disabled = false;
            }
        }
    });

    function parseDate(str) {
        // Asegúrate de que el formato es compatible con el constructor Date
        return new Date(str.replace(' ', 'T'));
    }

    function checkAvailability(doctorId, fechaInicio) {
        var fechaFin = new Date(fechaInicio.getTime() + 30 * 60000); // Suponiendo que cada cita dura 30 minutos

        for (var i = 0; i < appointmentsData.length; i++) {
            var appointmentStart = parseDate(appointmentsData[i].fechaInicio);
            var appointmentEnd = parseDate(appointmentsData[i].fechaFin);

            console.log("doctor:", appointmentsData[i].doctorId);
            console.log("fecha_inicioREAL:" + fechaInicio);
            console.log("fecha_inicio:" + appointmentStart);
            console.log("fecha_end:" + appointmentEnd);

            if (appointmentsData[i].doctorId == doctorId && fechaInicio < appointmentEnd && fechaFin > appointmentStart) {
                console.log("este no se pudo :((((");
                return false;
            }
        }
        return true;
    }
});
