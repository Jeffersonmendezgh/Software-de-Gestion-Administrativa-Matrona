document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("/catalogo/");
        const catalogo = await response.json();

        const contenedor = document.getElementById("catalogoProductos");
        contenedor.innerHTML = "";

        catalogo.forEach(item => {
            const productoHTML = `
            <div class="bg-orange-100 p-6 rounded-xl shadow-lg border border-gray-200 mb-8">
    <div class="flex flex-col md:flex-row gap-6">
     <div class="md:w-1/3 flex justify-center items-center bg-gray-50 rounded-lg p-4">
      <img src="https://res.cloudinary.com/dgrj6myiy/image/upload/v1757984968/beers_u44het.jpg" class="h-60   object-contain">
      </div>
    <!-- Detalles -->
    <div class="md:w-2/3 flex flex-col justify-between">
      <h3 class="text-2xl font-bold text-orange-700 mb-2">${item.inventario.nombre_bebida}</h3>
      <div class="grid grid-cols-2 gap-y-2 mb-4 text-gray-700">
        <div><span class="font-semibold">${item.precio_unidad}</div>
        <div><span class="font-semibold">${item.descripcion}</div>
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
            <select name="seleccionar_presentacion" id="seleccionar_presentacion"
              class="w-full p-2 border border-gray-300 rounded text-gray-700 bg-white">
              <option selected disabled>Seleccionar presentación</option>
              <option value="unidad">Unidad</option>
              <option value="sixpack">Sixpack</option>
              <option value="caja">Caja</option>
            </select>
            <input type="number" class="w-full p-2 border border-gray-300 rounded" placeholder="Cantidad">
          </div>
          <div class="flex items-end gap-2">
            <button class="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg">
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
        console.log("Error cargando el catalogo: ", error);
    }
});