//modal
function formatearPrecio(valor){
  if(!valor) return "$0";
  return valor.toLocaleString("es-CO", {
    style: "currency", currency: "COP", minimumFractionDigits: 0
  })
}
function mostrarCotizacion(data) {
   
  const modal = document.getElementById("modal-cotizacion");
  const contenido = document.getElementById("contenido-cotizacion");

  const c = data.catalogo; 

  contenido.innerHTML = `
    <div class="space-y-2">

      <p class="text-sm text-gray-500"># Cotización ${data.id_cotizacion}</p>

      <h3 class="text-lg font-bold text-orange-600">
        ${c.descripcion}
      </h3>

      <hr>

      <p><strong>Alcohol:</strong> ${c.alcohol}</p>
      <p><strong>Contenido:</strong> ${c.contenido} ml</p>

      <hr>

      <p><strong>Cantidad:</strong> ${data.cantidad_cotizado}</p>

      <p><strong>Precio unidad:</strong> $${formatearPrecio(c.precio_unidad)}</p>

      <hr>

      <p class="text-xl font-bold text-orange-700">
        Total: ${formatearPrecio(data.total_cotizacion)}
      </p>

      <p class="text-xs text-gray-400">
        Fecha: ${new Date(data.fecha_hora).toLocaleString()}
      </p>

    </div>
  `;

  modal.classList.remove("hidden");
}
//cerrar modal
document.getElementById("cerrar-modal").addEventListener("click", () => {
  document.getElementById("modal-cotizacion").classList.add("hidden");
});

// Delegación de eventos (clave para contenido dinámico)
document.addEventListener("click", async (e) => {

  // detectar botón de cotización
  const boton = e.target.closest("button");

  if (!boton) return;

  if (!boton.textContent.includes("Solicitar cotización")) return;

  //console.log("CLICK COTIZACION DETECTADO");

  // subir al contenedor del producto
  const producto = boton.closest("[data-id]");

  if (!producto) {
    console.error("No se encontró el producto");
    return;
  }

  const id_catalogo = producto.dataset.id;

  const tipo = producto.querySelector(".presentacion")?.value;
  const cantidad = producto.querySelector(".cantidad")?.value;

  console.log({
    id_catalogo,
    tipo,
    cantidad
  });

  // validación básica
  if (!tipo || !cantidad || tipo.includes("Seleccionar")) {
    alert("Selecciona presentación y cantidad");
    return;
  }

  try {
    const response = await fetch("/cotizacion/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        id_catalogo: parseInt(id_catalogo),
        tipo,
        cantidad: parseInt(cantidad)
      })
    });

    if (!response.ok) {
      const error = await response.json();
      console.error("Error backend:", error);
      alert(error.detail || "Error al crear cotización");
      return;
    }

    const data = await response.json();

  

    mostrarCotizacion(data);

  } catch (error) {
    console.error("Error de red:", error);
    alert("Error conectando con el servidor");
  }

});