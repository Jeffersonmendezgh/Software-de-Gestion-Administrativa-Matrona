async function cargarEmpleado() {
  const res = await fetch("http://127.0.0.1:8000/empleados/actual"); // sin id_usuario
  if (res.ok) {
    const data = await res.json();
    document.getElementById("salario").textContent = data.salario;
    document.getElementById("areaLaboral").textContent = data.area_laboral;
    document.getElementById("fechaPago").textContent = data.fecha_pago;
  }
}
cargarEmpleado();


/*document.addEventListener("DOMContentLoaded", async () => {
  const idUsuario = localStorage.getItem("idUsuario");
  const token = localStorage.getItem("token");

  if (!idUsuario || !token) {
    console.error("No hay sesión activa.");
    mostrarMensajeError("No hay información del empleado disponible.");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/empleados/${idUsuario}`, {
      headers: {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error al obtener los datos del empleado");
    }

    const datos = await response.json();
    console.log("Datos del empleado logeado:", datos);
    actualizarDatosEmpleado(datos);
  } catch (error) {
    console.error("Error al renderizar datos del empleado:", error);
    mostrarMensajeError("Error al cargar información del empleado.");
  }
});


function actualizarDatosEmpleado(datos) {
  // Obtener las etiquetas p dentro de cada tarjeta
  const salarioP = document.querySelector("#salario + p");
  const fechaPagoP = document.querySelector("#fechaPago + p");
  const areaLaboralP = document.querySelector("#areaLaboral + p");
  const nombreEmpleadoSpan = document.getElementById("nombreEmpleado");

  // Validar que existan los elementos
  if (!salarioP || !fechaPagoP || !areaLaboralP) {
    console.warn("No se encontraron los elementos de información del empleado.");
    return;
  }

  // Actualizar contenido
  salarioP.textContent = `COP ${new Intl.NumberFormat("es-CO").format(datos.salario)}`;
  areaLaboralP.textContent = datos.area_laboral;
  fechaPagoP.textContent = new Date(datos.fecha_contrato).toLocaleDateString("es-CO");

  if (nombreEmpleadoSpan && datos.usuario) {
    nombreEmpleadoSpan.textContent = `${datos.usuario.nombre} ${datos.usuario.apellido}`;
  }
}


function mostrarMensajeError(mensaje) {
  const bloqueInfoEmpleado = document.getElementById("bloqueInfoEmpleado");
  bloqueInfoEmpleado.innerHTML = `
    <p class="text-red-500 text-center mt-10">${mensaje}</p>
  `;
}
*/