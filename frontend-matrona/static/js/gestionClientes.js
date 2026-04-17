const listaClientes = document.getElementById('listaClientes');
const API_URL =  '/clientes/';

async function cargarClientes() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Error al obtener el cliente");

        const clientes = await response.json();
        renderizarClientes (clientes);
    } catch (error) {
        console.error("Error", error)
    }
}

function renderizarClientes(clientes) {
    
    listaClientes.innerHTML = "";

    clientes.forEach(cliente => {
        const tr = document.createElement("tr");

        tr.className = `
    hover:bg-gray-50 
    block md:table-row 
    mb-4 md:mb-0 
    border md:border-0 
    rounded-lg md:rounded-none 
    p-2 md:p-0
`;

tr.innerHTML = `
<td class="px-6 py-2 md:py-4 whitespace-nowrap block md:table-cell">
    <span class="md:hidden font-bold">Nombre: </span>
    ${cliente.usuario.nombre}
</td>

<td class="px-6 py-2 md:py-4 whitespace-nowrap block md:table-cell">
    <span class="md:hidden font-bold">Apellido: </span>
    ${cliente.usuario.apellido}
</td>

<td class="px-6 py-2 md:py-4 whitespace-nowrap block md:table-cell">
    <span class="md:hidden font-bold">Fecha: </span>
    ${cliente.fecha_registro}
</td>

<td class="px-6 py-2 md:py-4 block md:table-cell">
    <span class="md:hidden font-bold">Dirección: </span>
    ${cliente.usuario.direccion}
</td>

<td class="px-6 py-2 md:py-4 whitespace-nowrap block md:table-cell">
    <span class="md:hidden font-bold">Correo: </span>
    ${cliente.usuario.correo}
</td>
`;

        listaClientes.appendChild(tr);
    })
}

document.addEventListener("DOMContentLoaded", cargarClientes);