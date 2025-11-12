const listaClientes = document.getElementById('listaClientes');
const API_URL =  'http://127.0.0.1:8000/clientes/';

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

        tr.innerHTML = `
        <td class="px-6 py-4 whitespace-nowrap">${cliente.usuario.nombre}</td>
        <td class="px-6 py-4 whitespace-nowrap">${cliente.usuario.apellido}</td>
        <td class="px-6 py-4 whitespace-nowrap">${cliente.fecha_registro}</td>
        <td class="px-6 py-4">${cliente.usuario.direccion}</td>
        <td class="px-6 py-4 whitespace-nowrap">${cliente.usuario.correo}</td>
        `;

        listaClientes.appendChild(tr);
    })
}

document.addEventListener("DOMContentLoaded", cargarClientes);