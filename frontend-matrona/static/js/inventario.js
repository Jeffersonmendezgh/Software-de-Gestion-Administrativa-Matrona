// inventario.js
console.log(" inventario.js cargadondo correctamente");
//funcion para formatear precios
function formatearPrecio(valor){
  if(!valor) return "$0";
  return valor.toLocaleString("es-CO", {
    style: "currency", currency: "COP", minimumFractionDigits: 0
  })
  .replace(/\s/g, ""); //para quitar el espacio
}
async function cargarInventario() {
    try {
        const response = await fetch("http://127.0.0.1:8000/catalogo/");
        const inventario = await response.json();

        console.log(" Inventario recibido desde FastAPI:", inventario);

        const contenedor = document.getElementById("productosInventario");
        contenedor.innerHTML = ""; 

        inventario.forEach(item => {
            console.log("Item recibido:", item);
            const productoHTML = `
                <div class="border-b p-4 hover:bg-gray-50">
                    <div class="flex items-center justify-between">
                        <div>
                            <span class="font-semibold">${item.inventario.nombre_bebida}</span>
                            <span class="ml-4 text-gray-600">${item.inventario.cantidad_disponible} Unidades</span>
                        </div>
                        <div class="flex gap-2">
                            <input type="number" class="w-16 border px-2 py-1 rounded hidden" min="1" placeholder="0">
                            
                            <a href="/editar-inventario/${item.id_catalogo}" 
                       class="text-orange-600 hover:text-orange-800 px-3 py-1 rounded inline-block">
                       <i class="fas fa-edit mr-1"></i> Modificar
                    </a>
                    <button class="btn-detalles text-orange-600 hover:text-orange-800 px-3 py-1 rounded" 
                            data-id="${item.id_inventario}">
                    <i class="fas fa-plus mr-1"></i> Detalles
                    </button>
                    <button onclick="abrirModal(${item.id_inventario})"
                        class="text-green-600 hover:text-green-800 px-3 py-1 rounded">
                        <i class="fas fa-plus mr-1"></i> Agregar stock
                    </button>
                    <button onclick="eliminarProducto(${item.id_catalogo})" 
                        class="text-red-600 hover:text-red-800 px-3 py-1 rounded">
                        <i class="fas fa-trash mr-1"></i> Eliminar
                        </button>
                        </div>
                    </div>
                </div>
            `;
            contenedor.insertAdjacentHTML("beforeend", productoHTML);
        });

    } catch (error) {
        console.error(" Error al cargar inventario:", error);
    }
}

// Llamar la función al cargar la página
async function eliminarProducto(id_catalogo) {
    if (!confirm("¿Estás seguro de eliminar este producto?")) {
        return; // si el usuario cancela, no hace nada
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/catalogo/${id_catalogo}`, {
            method: "DELETE"
        });

        const data = await response.json();
        console.log("Eliminado:", data);

        // Recargar inventario después de eliminar
        cargarInventario();

    } catch (error) {
        console.error(" Error al eliminar producto:", error);
    }
}
//logica con modal para agregar nuevas cervezas
let inventarioSeleccionado = null; // Guardamos id de la cerveza a editar

function abrirModal(id) {
    inventarioSeleccionado = id;
    const modal = document.getElementById("modalStock");
    modal.classList.remove("hidden");
    modal.classList.add("flex");
}

function cerrarModal() {
    const modal = document.getElementById("modalStock");
    modal.classList.remove("flex");
    modal.classList.add("hidden");
    document.getElementById("modalStockInput").value = "";
}


async function confirmarStock() {
    const cantidad = parseInt(document.getElementById("modalStockInput").value);

    if (cantidad > 0) {
        await fetch(`http://127.0.0.1:8000/inventario/agregar-stock/${inventarioSeleccionado}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ unidades: cantidad })
        });

        cerrarModal();
        cargarInventario(); // recargar lista
    } else {
        alert("Ingrese una cantidad válida");
    }
}

//bloque para agregar la funcion de detalles al bloque de codigo
// Detectar click en los botones de Detalles
document.getElementById("productosInventario").addEventListener("click", async (e) => {
  const btn = e.target.closest(".btn-detalles"); // busca el botón con clase
  if (!btn) return;

  const id = btn.dataset.id; // toma el data-id del botón
  console.log(" Click en Detalles de ID:", id);

  try {
    const res = await fetch(`/inventario/${id}`);
    if (!res.ok) throw new Error("Error al obtener detalles");
    const item = await res.json();

    // Actualizar el bloque de detalles
    document.getElementById("detalles").innerText = `Detalles ${item.nombre_bebida}`;
    document.getElementById("stock").innerText = `${item.cantidad_disponible} Unidades disponibles`;
    document.getElementById("alcohol").innerText = `${item.catalogo[0].alcohol} Vol Alcohol`;
    document.getElementById("contendio").innerText = `${item.catalogo[0].contenido} Ml de Contenido`;

    document.getElementById("costoUnidad").innerText = item.catalogo[0].precio_unidad ? formatearPrecio(item.catalogo[0].precio_unidad) : '--';
    document.getElementById("costoSixpack").innerText = item.catalogo[0].precio_sixpack ? formatearPrecio(item.catalogo[0].precio_sixpack): '--';
    document.getElementById("costoCaja").innerText = item.catalogo[0].precio_caja ? formatearPrecio(item.catalogo[0].precio_caja): '--';

    
    console.log(" Detalles recibidos:", item);
  } catch (err) {
    console.error(err);
    alert("No se pudieron cargar los detalles.");
  }
});

cargarInventario();

