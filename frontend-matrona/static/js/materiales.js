document.addEventListener("DOMContentLoaded", function() {
  const API_URL = "http://127.0.0.1:8000/api/materiales"; // endpoint backend put
  const form = document.querySelector("form");
  const modal = document.getElementById("miModal");
  let idMaterialActual = null; // Para guardar el ID cuando editamos

  //Cargar materiales desde el backend al iniciar
  async function cargarMateriales() {
    const response = await fetch(API_URL);
    const materiales = await response.json();

    // Limpiamos las tablas
    document.querySelector("#tabla-produccion tbody").innerHTML = "";
    document.querySelector("#tabla-envasado tbody").innerHTML = "";

    materiales.forEach(mat => {
      agregarFila(mat.tipo_material, mat.cantidad_a_agregar, mat.id_materiales, mat.actividad);
    });

    agregarEventosBotones();
  }

  //Agregar material (POST)
  form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const actividad = document.getElementById("actividad").value;
    const material = document.getElementById("tipoMaterial").value;
    const valor = document.getElementById("cantidadAgregar").value;

    if (!material || !valor) {
      alert("Por favor completa todos los campos");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tipo_material: material,
          cantidad_a_agregar: valor,
          actividad: actividad
        })
      });

      if (!response.ok) {
    const text = await response.text();
    throw new Error(`Error HTTP ${response.status}: ${text}`);
  }
      const nuevoMaterial = await response.json();
  

      // Agregamos visualmente a la tabla correspondiente
      agregarFila(nuevoMaterial.tipo_material, nuevoMaterial.cantidad_a_agregar, nuevoMaterial.id_materiales, actividad);
      agregarEventosBotones();
  
      // Limpiamos inputs
      document.getElementById("tipoMaterial").value = "";
      document.getElementById("cantidadAgregar").value = "";

    } catch (error) {
      console.error("Error:", error);
      alert("Hubo un problema al agregar el material.");
    }
  });

  // Crear fila en la tabla
  function agregarFila(material, valor, id, actividad = "producir") {
    const tablaDestino = actividad === "producir"
      ? document.querySelector("#tabla-produccion tbody")
      : document.querySelector("#tabla-envasado tbody");

    const nuevaFila = document.createElement("tr");
    nuevaFila.setAttribute("data-id", id);
    nuevaFila.innerHTML = `
      <td class="p-3">${material}</td>
      <td class="p-3">${valor}</td>
      <td class="p-3 text-center">
        <button class="text-blue-600 hover:text-blue-800 mr-2 editar-btn"><i class="fas fa-edit"></i></button>
        <button class="text-red-600 hover:text-red-800 eliminar-btn"><i class="fas fa-trash-alt"></i></button>
      </td>
    `;
    tablaDestino.appendChild(nuevaFila);
  }

  //Agregar eventos a los botones (editar y eliminar)
  function agregarEventosBotones() {
    document.querySelectorAll(".editar-btn").forEach(boton => {
      if (!boton.hasAttribute("data-event-added")) {
        boton.setAttribute("data-event-added", "true");
        boton.addEventListener("click", function() {
          const fila = boton.closest("tr");
          idMaterialActual = fila.getAttribute("data-id");
          document.getElementById("campoNombre").value = fila.cells[0].textContent;
          document.getElementById("campoValor").value = fila.cells[1].textContent;

          modal.classList.remove("hidden");
          modal.classList.add("flex", "items-center", "justify-center");
        });
      }
    });

    document.querySelectorAll(".eliminar-btn").forEach(boton => {
      if (!boton.hasAttribute("data-event-added")) {
        boton.setAttribute("data-event-added", "true");
        boton.addEventListener("click", async function() {
          const fila = boton.closest("tr");
          const id = fila.getAttribute("data-id");

          if (confirm("¿Seguro que deseas eliminar este material?")) {
            try {
              const response = await fetch(`${API_URL}/${id}`, {
                method: "DELETE"
              });

              if (!response.ok) throw new Error("Error al eliminar");

              fila.remove();
            } catch (error) {
              console.error("Error al eliminar:", error);
            }
          }
        });
      }
    });
  }

  //Editar material (PUT desde el modal) cambie los ids en html tener presente
  document.getElementById("guardar").addEventListener("click", async function() {
    const nuevoNombre = document.getElementById("campoNombre").value;
    const nuevoValor = document.getElementById("campoValor").value;

    if (!idMaterialActual) return;

    try {
      const response = await fetch(`${API_URL}/${idMaterialActual}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tipo_material: nuevoNombre,
          cantidad_a_agregar: nuevoValor
        })
      });

      if (!response.ok) throw new Error("Error al actualizar material");

      await cargarMateriales(); // Refresca tabla
      cerrarModal();

    } catch (error) {
      console.error("Error al actualizar:", error);
    }
  });

  //Cancelar en modal
  document.getElementById("cancelar").addEventListener("click", cerrarModal);

  function cerrarModal() {
    modal.classList.add("hidden");
    modal.classList.remove("flex", "items-center", "justify-center");
  }

  //Inicializar
  cargarMateriales();
});

//mostrar usuario
function mostrarUsuarioActual() {
  const nombre = localStorage.getItem("nombreUsuario");
  const apellido = localStorage.getItem("apellidoUsuario");
  const rol = localStorage.getItem("rolUsuario");

  const nombreSpan = document.getElementById("nombreUsuario");
  const rolSpan = document.getElementById("rolUsuario");

  if (nombre && apellido) {
    nombreSpan.textContent = `${nombre} ${apellido}`
  }
  if (rol) {
    rolSpan.textContent = `${rol}`
  }
}
mostrarUsuarioActual()