document.addEventListener("DOMContentLoaded", () => {
  const formularioProveedor = document.getElementById("formularioProveedor");
  const btnAgregar = document.getElementById("btn-agregarProveedor");
  const mensaje = document.getElementById("mensaje");
  const mensajeError = document.getElementById("mensajeError");
  const tablaProveedores = document.getElementById("filaProveedores");
  const BASE_URL = "http://127.0.0.1:8000/proveedor/";

  // Función para mostrar mensaje de éxito o error
  function mostrarMensaje(texto, tipo = "exito") {
    if (tipo === "exito") {
      mensaje.textContent = texto;
      mensajeError.classList.add("hidden");
      mensaje.classList.remove("hidden");
    } else {
      mensajeError.textContent = texto;
      mensaje.classList.add("hidden");
      mensajeError.classList.remove("hidden");
    }
  }

  //  Función para renderizar la tabla
  function renderizarProveedores(proveedores) {
    tablaProveedores.innerHTML = ""; // Limpiar la tabla

    if (proveedores.length === 0) {
      tablaProveedores.innerHTML = `
        <tr><td colspan="6" class="text-center text-gray-500 py-4">No hay proveedores registrados.</td></tr>
      `;
      return;
    }

    proveedores.forEach((p) => {
      const fila = document.createElement("tr");
      fila.classList.add("hover:bg-orange-100");

      fila.innerHTML = `
        <td class="px-6 py-4 whitespace-nowrap text-gray-900">${p.nombre_proveedor}</td>
        <td class="px-6 py-4 whitespace-nowrap text-gray-900">${p.material_que_provee}</td>
        <td class="px-6 py-4 whitespace-nowrap text-gray-900">${p.cantidadM}</td>
        <td class="px-6 py-4 whitespace-nowrap text-gray-900">${p.frecuencia_entrega}</td>
        <td class="px-6 py-4 whitespace-nowrap text-gray-900">${p.telefono}</td>
        <td class="px-6 py-4 whitespace-nowrap text-gray-900">${p.direccion_proveedor}</td>
      `;

      tablaProveedores.appendChild(fila);
    });
  }

  // Obtener lista de proveedores desde el backend
  async function cargarProveedores() {
    try {
      const res = await fetch(BASE_URL);
      if (!res.ok) throw new Error("Error al obtener proveedores");
      const data = await res.json();
      renderizarProveedores(data);
    } catch (error) {
      console.error(" Error al cargar proveedores:", error);
      mostrarMensaje("Error al cargar proveedores.", "error");
    }
  }

  // Registrar evento del botón para enviar el formulario
  btnAgregar.addEventListener("click", () => {
    formularioProveedor.requestSubmit();
  });

  // Envío del formulario (POST)
  formularioProveedor.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      nombre_proveedor: document.getElementById("nombreProveedor").value,
      material_que_provee: document.getElementById("materialQueProvee").value,
      cantidadM: document.getElementById("cantidadM").value,
      telefono: document.getElementById("telefonoProveedor").value,
      direccion_proveedor: document.getElementById("direccionProveedor").value,
      frecuencia_entrega: document.getElementById("frecuenciaEntrega").value
    };

    try {
      const response = await fetch(BASE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Error al crear proveedor");
      }

      const nuevoProveedor = await response.json();
      mostrarMensaje(`Proveedor ${nuevoProveedor.nombre_proveedor} agregado correctamente.`);
      formularioProveedor.reset();

      //  Recargar tabla sin recargar la página
      await cargarProveedores();

    } catch (error) {
      console.error(" Error al crear proveedor:", error);
      mostrarMensaje("Error al registrar proveedor.", "error");
    }
  });

  // Cargar todos los proveedores al iniciar
  cargarProveedores();
});
