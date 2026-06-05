document.addEventListener("DOMContentLoaded", function(){

function formatearPrecio(valor){
    
  if(!valor) return "$0";
  const numero = parseFloat(valor);

  return numero.toLocaleString("es-CO", {
    style: "currency", currency: "COP", minimumFractionDigits: 0
  })
  .replace(/\s/g, ""); //para quitar el espacio
}

async function cargarStatsPedidos() {
    const response = await fetch("/clientes/mis-pedidos/stats");
    const data = await response.json();

    document.getElementById("total-pedidos").textContent = data.total;
    document.getElementById("entregados").textContent = data.entregados;
    document.getElementById("pendientes").textContent = data.pendientes;
}


async function cargarPedido() {
    
    const response = await fetch("/clientes/mis-pedidos");
    const clientePedido = await response.json();

    const contenedorPedidos = document.getElementById("contenedor-principal-pedidos");
    contenedorPedidos.innerHTML = "";

    // ordenar: pendientes primero
    clientePedido.sort((a, b) => {
        if (a.estado === b.estado) return 0;
        if (a.estado.toLowerCase() === "pendiente") return -1;
        return 1;
    });

    clientePedido.forEach(item => {

        // colores dinámicos de acuerdo al pedido
        const esEntregado = item.estado.toLowerCase() === "entregado";

        const estadoClase = esEntregado
            ? "bg-green-100 text-green-800"
            : "bg-red-100 text-red-800";

        const icono = esEntregado
            ? "fa-check-circle"
            : "fa-clock";

        const pedidoHTML = `
            <div class="flex justify-between items-start border-b pb-3 mb-3">
                <div>
                    <div class="flex items-center mb-1">
                        <span class="font-bold text-orange-600 mr-2">
                            Numero de Pedido ${item.id_pedido}
                        </span>
                        <span class="px-3 py-1 rounded-full text-xs font-semibold ${estadoClase} flex items-center">
                            <i class="fas ${icono} mr-1"></i> ${item.estado}
                        </span>
                    </div>

                    <p class="text-sm text-gray-500 mb-2">${item.fecha}</p>
                    
                    <div class="flex items-center text-sm text-gray-700 mb-1">
                        <i class="fas fa-beer mr-2 text-orange-500"></i>
                        <span>
                            ${item.detalles.map(d => ` <div>Unidades ${d.cantidad} - ${d.nombre_cerveza}</div>`).join("")}
                        </span>
                    </div>
                </div>

                <div class="text-right">
                    <p class="text-lg font-bold text-orange-600">
                        ${formatearPrecio(item.total)}
                    </p>
                </div>
            </div>
        `;

        contenedorPedidos.insertAdjacentHTML("beforeend", pedidoHTML);
    });


}


cargarPedido()
cargarStatsPedidos()
})
