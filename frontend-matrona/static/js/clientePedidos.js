document.addEventListener("DOMContentLoaded", function(){

function formatearPrecio(valor){
    
  if(!valor) return "$0";
  const numero = parseFloat(valor);

  return numero.toLocaleString("es-CO", {
    style: "currency", currency: "COP", minimumFractionDigits: 0
  })
  .replace(/\s/g, ""); //para quitar el espacio
}



async function cargarPedido() {
    
    const response = await fetch("http://127.0.0.1:8000/clientes/mis-pedidos");
    const clientePedido = await response.json();
    console.log("que me trae",clientePedido)
    const contenedorPedidos = document.getElementById("contenedor-principal-pedidos");

    contenedorPedidos.innerHTML = "";
    clientePedido.forEach(item => {
       const pedidoHTML = `
                        <div class="flex justify-between items-start">
                            <div>
                                <div class="flex items-center mb-1">
                                    <span class="font-bold text-orange-600 mr-2"> id pedido ${item.id_pedido}</span>
                                    <span class="px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800 flex items-center">
                                        <i class="fas fa-check-circle mr-1"></i> Reclamado
                                    </span>
                                </div>
                                <p class="text-sm text-gray-500 mb-2">28/07/2025 - 10:45 AM</p>
                                
                                <div class="flex items-center text-sm text-gray-700 mb-1">
                                    <i class="fas fa-beer mr-2 text-orange-500"></i>
                                    <span>${item.detalles[0].cantidad} unidades - ${item.detalles[0].nombre_cerveza}</span>
                                </div>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-orange-600">${formatearPrecio(item.total)}</p>
                            </div>
                        </div>
       `;
       contenedorPedidos.insertAdjacentHTML("beforeend", pedidoHTML);

    });

}


cargarPedido()
})
