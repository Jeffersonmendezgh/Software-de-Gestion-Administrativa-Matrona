// =============================
// 📦 Función para enviar pedidos
// =============================
async function enviarPedido(clienteId, items) {
    // items = [{ id_catalogo: 1, cantidad: 2 }, ...] 
    const body = { id_cliente: clienteId, items };

    try {
        const res = await fetch("/pedidos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            // Si el backend devuelve error, lo mostramos
            const err = await res.json();
            alert("❌ Error: " + (err.detail || "Error al crear pedido"));
            return;
        }

        const data = await res.json();
        alert("✅ Pedido creado con ID: " + data.id_pedidos);

        // Opcional: también podrías renderizarlo localmente
        // aunque normalmente esto lo hace la notificación por WS.
        // renderPedido(data);

    } catch (e) {
        console.error("Error enviando pedido:", e);
        alert("⚠️ Error de red");
    }
}

// =============================
// 🔔 Función para renderizar pedidos en la interfaz
// =============================
function renderPedido(pedido) {
    const cont = document.querySelector(".contenedor_pedidos");

    const div = document.createElement("div");
    div.className = "flex bg-orange-200 shadow-xl p-3 rounded border-l-4 border-orange-500";

    div.innerHTML = `
        <div class="w-1/4">${pedido.cliente?.nombre || "Cliente desconocido"} ${pedido.cliente?.apellido || ""}</div>
        <div class="w-1/4">${pedido.detalles[0]?.cantidad_pedido_uds || 0}</div>
        <div class="w-1/4">${pedido.detalles[0]?.presentacion || "N/A"}</div>
        <div class="w-1/4 text-right font-semibold ${pedido.estado === "entregado" ? "text-green-600" : "text-red-600"}">
            ${pedido.estado === "pendiente" 
                ? `<button id="btn-pedido-${pedido.id_pedidos}" class="bg-orange-400 text-black rounded-xl p-1">Entregar</button> Pendiente`
                : "Entregado"}
        </div>
    `;

    cont.prepend(div);

    // Enganchar el botón "Entregar" si existe
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
                div.querySelector("div:last-child").textContent = "Entregado";
                div.querySelector("div:last-child").classList.remove("text-red-600");
                div.querySelector("div:last-child").classList.add("text-green-600");
            }
        });
    }
}

// =============================
// 📡 WebSocket para notificaciones en tiempo real
// =============================
const ws = new WebSocket("ws://" + location.host + "/ws/pedidos");

// Cuando se conecta
ws.onopen = () => console.log("✅ WebSocket conectado");

// Cuando llega un mensaje
ws.onmessage = ev => {
    const msg = JSON.parse(ev.data);

    if (msg.type === "new_order") {
        console.log("🔔 Nuevo pedido recibido:", msg.data);
        renderPedido(msg.data);
    }
};

//Cargar pedidos existentes
async function cargarPedidos() {
    try {
        const res = await fetch("/pedidos");
        if (!res.ok) throw new Error("Error al cargar pedidos")

        const pedidos = await res.json();
        pedidos.forEach(p => renderPedido(p));
    } catch (e){
        console.error("no se pudieron cargar los pedidos:", e)
    }
    
}
// Cuando se desconecta
ws.onclose = () => console.warn("⚠️ WebSocket cerrado");

// Si hay error
ws.onerror = err => console.error("❌ WebSocket error:", err);

document.addEventListener("DOMContentLoaded", cargarPedidos);