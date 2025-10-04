const contenedor = document.getElementById("catalogoProductos");

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/catalogo/");
    const catalogo = await response.json();

    contenedor.innerHTML = "";

    catalogo.forEach(item => {
      const productoHTML = `
        <div class="bg-orange-100 p-6 rounded-xl shadow-lg border border-gray-200 mb-8" data-id="${item.id_catalogo}">
          <div class="flex flex-col md:flex-row gap-6">
            <!-- Imagen -->
            <div class="md:w-1/3 flex justify-center items-center bg-gray-50 rounded-lg p-4">
              <img src="https://res.cloudinary.com/dgrj6myiy/image/upload/v1757984968/beers_u44het.jpg" class="h-60 object-contain">
            </div>
            <!-- Detalles -->
            <div class="md:w-2/3 flex flex-col justify-between">
              <h3 class="text-2xl font-bold text-orange-700 mb-2">${item.inventario.nombre_bebida}</h3>
              <div class="grid grid-cols-2 gap-y-2 mb-4 text-gray-700">
                <div><span class="font-semibold">${item.precio_unidad}</span></div>
                <div><span class="font-semibold">${item.descripcion}</span></div>
                <div><span class="font-semibold">${item.alcohol}</span></div>
                <div><span class="font-semibold">${item.contenido}</span> ML</div>
                <div><span class="font-semibold">Vencimiento:</span> 20 - 09 - 2026</div>
              </div>
              <div class="mb-4">
                <h4 class="font-semibold text-gray-800 mb-2">Presentaciones:</h4>
                <div class="flex flex-wrap gap-3 text-sm">
                  <span class="bg-orange-100 text-orange-700 px-3 py-1 rounded-lg">${item.precio_unidad}</span>
                  <span class="bg-orange-100 text-orange-700 px-3 py-1 rounded-lg">${item.precio_sixpack}</span>
                  <span class="bg-orange-100 text-orange-700 px-3 py-1 rounded-lg">${item.precio_caja}</span>
                </div>
              </div>
              <div class="border-t pt-4 mt-2">
                <h4 class="font-semibold text-gray-800 mb-2">Realizar pedido</h4>
                <div class="flex flex-col md:flex-row gap-4">
                  <div class="flex-1 space-y-2">
                    <select class="presentacion w-full p-2 border border-gray-300 rounded text-gray-700 bg-white">
                      <option selected disabled>Seleccionar presentación</option>
                      <option value="unidad">Unidad</option>
                      <option value="sixpack">Sixpack</option>
                      <option value="caja">Caja</option>
                    </select>
                    <input type="number" class="cantidad w-full p-2 border border-gray-300 rounded" placeholder="Cantidad">
                  </div>
                  <div class="flex items-end gap-2">
                    <button class="btn-reservar bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg">
                      Reservar pedido
                    </button>
                    <button class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg">
                      Solicitar cotización
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
      contenedor.insertAdjacentHTML("beforeend", productoHTML);
    });
  } catch (error) {
    console.error("Error cargando el catalogo: ", error);
  }
});

// Delegación de eventos para pedidos
contenedor.addEventListener("click", async (e) => {
  if (e.target.classList.contains("btn-reservar")) {
    const card = e.target.closest("div.bg-orange-100");
    const presentacion = card.querySelector(".presentacion").value;
    const cantidad = parseInt(card.querySelector(".cantidad").value);
    const productoId = card.dataset.id;

    if (!presentacion || !cantidad || cantidad <= 0) {
      alert("Selecciona presentación y una cantidad válida");
      return;
    }

    // Conversión de presentaciones a unidades
    let unidadesTotales = 0;
    if (presentacion === "unidad") unidadesTotales = cantidad;
    if (presentacion === "sixpack") unidadesTotales = cantidad * 6;
    if (presentacion === "caja") unidadesTotales = cantidad * 24;

    // Construcción del pedido (conforme a PedidoCreate)
    const pedido = {
      items: [
        {
          id_catalogo: parseInt(productoId),
          cantidad_pedido_uds: parseInt(unidadesTotales),
          presentacion: String(presentacion)
        }
      ]
    };

    console.log("Pedido JSON:", JSON.stringify(pedido, null, 2));

    try {
      const res = await fetch("/pedidos/", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify(pedido)
      });

      if (res.ok) {
        const data = await res.json();
        alert(` Pedido realizado: ${cantidad} ${presentacion}(s) = ${unidadesTotales} cervezas`);
        console.log("Respuesta backend:", data);
      } else {
        const errorData = await res.json();
        console.error("Error en respuesta:", errorData);
        alert(" Error al realizar pedido: " + (errorData.detail || JSON.stringify(errorData)));
      }
    } catch (err) {
      console.error("Error enviando pedido:", err);
      alert(" Error al enviar el pedido");
    }
  }
});
