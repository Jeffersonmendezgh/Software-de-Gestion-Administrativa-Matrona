document.addEventListener("DOMContentLoaded", () => {
const BASE_URL_EMPLEADOS = "http://127.0.0.1:8000/empleados/";

let empleadosCache = []; // cache para poder buscar por id
const contenedorEmpleados = document.getElementById("tarjetaEmpleado");
const formularioEmpleados = document.getElementById("formularioEmpleado");
const formEditarEmpleado = document.getElementById("formEditarEmpleado");
const btnGuardarCambios = document.getElementById("btnGuardarCambios")
//campos del form
const nombreEmpleado = document.getElementById("nombreEmpleado");
const fechaContratacion = document.getElementById("fechaContratacion");
const areaLaboral = document.getElementById("areaLaboral");
const salario = document.getElementById("salario");
const fechaPago = document.getElementById("fechaPago");
const telefonoEmpleado = document.getElementById("telefonoEmpleado")
// Función para renderizar las tarjetas de empleados

let idEmpleadoSeleccionado = null; // Guardamos el id del empleado que se está editando para el patch

function renderizarEmpleados(empleados) {
    empleadosCache = empleados;
    contenedorEmpleados.innerHTML = ''; // Limpiamos el contenedor

    empleados.forEach((e) => {
        // Creamos la tarjeta de cada empleado
        const tarjeta = `
            <div class="bg-white p-4 rounded-lg shadow-md border border-orange-200 hover:shadow-lg transition">
                <div class="flex items-center mb-3">
                    <div class="bg-orange-100 p-3 rounded-full mr-3">
                        <i class="fas fa-user text-orange-600"></i>
                    </div>
                    <h3 class="font-bold text-lg">${e.usuario.nombre} ${e.usuario.apellido}</h3>
                </div>

                <div class="space-y-2 text-sm">
                    <div class="flex items-center">
                        <i class="fas fa-calendar-day text-orange-500 mr-2 w-5"></i>
                        <span>Fecha de Contratación: ${e.fecha_contratacion || '---'}</span>
                    </div>
                    <div class="flex items-center">
                        <i class="fas fa-briefcase text-orange-500 mr-2 w-5"></i>
                        <span>Área Laboral: ${e.area_laboral || '---'}</span>
                    </div>
                    <div class="flex items-center">
                        <i class="fas fa-money-bill-wave text-orange-500 mr-2 w-5"></i>
                        <span>Salario: ${e.salario || '---'}</span>
                    </div>
                    <div class="flex items-center">
                        <i class="fas fa-calendar-check text-orange-500 mr-2 w-5"></i>
                        <span>Fecha de Pago: ${e.fecha_pago || '---'}</span>
                    </div>
                    <div class="flex items-center">
                        <i class="fas fa-phone text-orange-500 mr-2 w-5"></i>
                        <span>Teléfono: ${e.telefono_empleado || '---'}</span>
                    </div>
                </div>

                <div class="mt-4 flex justify-end space-x-2">
                    <button class="editar p-2 text-orange-600 hover:bg-orange-100 rounded-full"data-id="${e.id_empleado}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="p-2 text-red-600 hover:bg-red-100 rounded-full"data-id="${e.id_empleado}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;

        // Insertamos la tarjeta en el contenedor
        contenedorEmpleados.insertAdjacentHTML("beforeend", tarjeta);
    });
    //vinculacion del evento de edicion
    document.querySelectorAll(".editar").forEach((btn) => {
        btn.addEventListener("click", (ev) => {
            const id = ev.currentTarget.dataset.id;
            const empleado = empleadosCache.find(emp => emp.id_empleado == id)
            abrirFormulario(empleado)
        });
    });
}
//mostrar formulario con datos cargados
function abrirFormulario(empleado) {
    idEmpleadoSeleccionado = empleado.id_empleado; // guardamos solo el ID
    formularioEmpleados.classList.remove("hidden");

    // rellenar los campos con los datos del empleado
    nombreEmpleado.value = empleado.nombre || '';
    fechaContratacion.value = empleado.fecha_contratacion || '';
    areaLaboral.value = empleado.area_laboral || '';
    salario.value = empleado.salario || '';
    fechaPago.value = empleado.fecha_pago || '';
    telefonoEmpleado.value = empleado.telefono_empleado || '';
}
//PATCH para guardar 
formEditarEmpleado.addEventListener("submit", async (e) => {
    e.preventDefault();

    const datosActualizados = {
        nombre: nombreEmpleado.value,
        fecha_contratacion: fechaContratacion.value,
        area_laboral: areaLaboral.value,
        salario: salario.value,
        fecha_pago: fechaPago.value,
        telefono_empleado: telefonoEmpleado.value
    };
    try {
        const res = await fetch(`${BASE_URL_EMPLEADOS}${idEmpleadoSeleccionado}`, {
           method: "PATCH",
           headers: {"Content-Type": "application/json"},
           body: JSON.stringify(datosActualizados) 
        });

        if (!res.ok) throw new Error("Error al actualizar el empleado")

        alert("Empleado actualizado correctamente");
        formularioEmpleados.classList.add("hidden");
        await cargarEmpleados()//para recargar la lista

    } catch (error) {
        console.error(error);
        alert("Hubo un problema al actuyalizar el empleado");
    }
})

// Función para obtener los empleados desde el backend
async function cargarEmpleados() {
    try {
        const res = await fetch(BASE_URL_EMPLEADOS);
        if (!res.ok) throw new Error("Error al obtener los empleados");
        const data = await res.json();
        renderizarEmpleados(data);
    } catch (error) {
        console.error("Error al cargar empleados:", error);
    }
}

// Ejecutamos la carga al iniciar
cargarEmpleados();
});
//editar empleado

