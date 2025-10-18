//  Función para enviar pedidos
async function enviarPedido(clienteId, items) {
    // items 
    const body = { id_cliente: clienteId, items };

    try {
        const res = await fetch("/pedidos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(" Error: " + (err.detail || "Error al crear pedido"));
            return;
        }

        const data = await res.json();
        alert(" Pedido creado con ID: " + data.id_pedidos);

    } catch (e) {
        console.error("Error enviando pedido:", e);
        alert(" Error de red");
    }
}

//  Renderizar pedido en pantalla
function renderPedido(pedido) {
    const cont = document.querySelector(".contenedor_pedidos");

    const div = document.createElement("div");
    div.className = "flex bg-orange-200 shadow-xl p-3 rounded border-l-4 border-orange-500 mb-2";
//los operadores ?. me sirven para evitar errores en caso de que algun campo vena null
    div.innerHTML = `
        <div class="w-1/4">${pedido.cliente?.usuario.nombre || "Cliente desconocido"} ${pedido.cliente?.usuario.apellido || ""}</div>
        <div class="w-1/4">${pedido.detalles?.[0]?.cantidad_pedido_uds || 0}</div>
        <div class="w-1/4">${pedido.detalles?.[0]?.nombre_bebida || "Sin nombre"}</div>
        <div class="w-1/4">${pedido.detalles?.[0]?.presentacion || "N/A"}</div>
        <div class="w-1/4 text-right font-semibold ${pedido.estado === "entregado" ? "text-green-600" : "text-red-600"}">
            ${pedido.estado === "pendiente" 
                ? `<button id="btn-pedido-${pedido.id_pedidos}" class="bg-orange-400 text-black rounded-xl p-1">Entregar</button> Pendiente`
                : "Entregado"}
        </div>
    `;

    cont.prepend(div);

    //  Enganchar botón Entregar
    const btn = div.querySelector(`#btn-pedido-${pedido.id_pedidos}`);
    if (btn) {
        btn.addEventListener("click", async () => {
            const res = await fetch(`/pedidos/${pedido.id_pedidos}/estado`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estado: "entregado" })
            });

            if (res.ok) {
                btn.remove();
                const estadoDiv = div.querySelector("div:last-child");
                estadoDiv.textContent = "Entregado";
                estadoDiv.classList.remove("text-red-600");
                estadoDiv.classList.add("text-green-600");
            }
        });
    }
}

// WebSocket para notificaciones en tiempo real
const ws = new WebSocket(
    (location.protocol === "https:" ? "wss://" : "ws://") + location.host + "/ws/pedidos"
);

ws.onopen = () => console.log(" WebSocket conectado");

ws.onmessage = ev => {
    const msg = JSON.parse(ev.data);
    if (msg.type === "new_order") {
        console.log(" Nuevo pedido recibido:", msg.data);
        renderPedido(msg.data);
    }
};

ws.onclose = () => console.warn(" WebSocket cerrado");
ws.onerror = err => console.error(" WebSocket error:", err);

//  Cargar pedidos existentes al iniciar
async function cargarPedidos() {
    try {
        const res = await fetch("/pedidos");
        if (!res.ok) throw new Error("Error al cargar pedidos");

        const pedidos = await res.json();
        pedidos.forEach(p => renderPedido(p));
    } catch (e) {
        console.error("No se pudieron cargar los pedidos:", e);
    }
}

document.addEventListener("DOMContentLoaded", cargarPedidos);

//funcion para mostrar infoadmin
function mostrarUsuarioActual() {
  const nombre = localStorage.getItem("nombreUsuario");
  const apellido = localStorage.getItem("apellidoUsuario");
  const rol = localStorage.getItem("rolUsuario");

  const nombreSpan = document.getElementById("nombreUsuario");
  const rolSpan = document.getElementById("rolUsuario");

  if (!nombreSpan || !rolSpan) {
    console.warn(" Elementos del usuario no encontrados en el HTML.");
    return;
  }

  if (nombre && apellido) {
    nombreSpan.textContent = `${nombre} ${apellido}`;
  } else {
    nombreSpan.textContent = "Invitado";
  }

  if (rol) {
    rolSpan.textContent = `(Admin${rol})`;
  } else {
    rolSpan.textContent = "";
  }
}
mostrarUsuarioActual()

//funciona para cerrar sesion
const logoutBtn = document.getElementById("logoutBtn")

  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.clear();
      window.location.href = "/auth/login/";
    });
  }
