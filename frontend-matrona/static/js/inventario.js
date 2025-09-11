// inventario.js
console.log("✅ inventario.js cargado correctamente");

async function cargarInventario() {
    try {
        const response = await fetch("http://127.0.0.1:8000/catalogo/");
        const inventario = await response.json();

        console.log("📦 Inventario recibido desde FastAPI:", inventario);

        const contenedor = document.getElementById("productosInventario");
        contenedor.innerHTML = ""; // Limpiar el contenedor antes de llenarlo

        inventario.forEach(item => {
            console.log("🔎 Item recibido:", item);
            const productoHTML = `
                <div class="border-b p-4 hover:bg-gray-50">
                    <div class="flex items-center justify-between">
                        <div>
                            <span class="font-semibold">${item.inventario.nombre_bebida}</span>
                            <span class="ml-4 text-gray-600">${item.inventario.cantidad_disponible} Unidades</span>
                        </div>
                        <div class="flex gap-2">
                            <input type="number" class="w-16 border px-2 py-1 rounded hidden" min="1" placeholder="0">
                            <button class="text-orange-600 hover:text-orange-800 px-3 py-1 rounded">
                                <i class="fas fa-plus mr-1"></i> Detalles
                            </button>
                            <a href="/editar-inventario/${item.id_catalogo}" 
                       class="text-orange-600 hover:text-orange-800 px-3 py-1 rounded inline-block">
                       <i class="fas fa-edit mr-1"></i> Modificar
                    </a>
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
        console.error("❌ Error al cargar inventario:", error);
    }
}

// Llamar la función al cargar la página
async function eliminarProducto(id_catalogo) {
    if (!confirm("⚠️ ¿Estás seguro de eliminar este producto?")) {
        return; // si el usuario cancela, no hace nada
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/catalogo/${id_catalogo}`, {
            method: "DELETE"
        });

        const data = await response.json();
        console.log("✅ Eliminado:", data);

        // Recargar inventario después de eliminar
        cargarInventario();

    } catch (error) {
        console.error("❌ Error al eliminar producto:", error);
    }
}
//logica con modal para agregar nuevas cervezas
let inventarioSeleccionado = null; // Guardamos id de la cerveza a editar

function abrirModal(id) {
    inventarioSeleccionado = id; // guardamos qué cerveza vamos a modificar
    document.getElementById("modalStock").classList.remove("hidden");
}

function cerrarModal() {
    document.getElementById("modalStock").classList.add("hidden");
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
cargarInventario();

