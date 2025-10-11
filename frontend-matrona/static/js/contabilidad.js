// contabilidad.js
document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "http://127.0.0.1:8000/contabilidad";
  const tbody = document.getElementById("filaContable"); //  tbody tomare este bloque 
  const totalUnidadesEl = document.getElementById("totalUnidades");
  const totalIngresosEl = document.getElementById("totalIngresos");
  const ingresosPorProductoEl = document.getElementById("ingresosPorProducto");

  // formatea número a moneda local 
  function formatCurrency(value) {
    try {
      const n = Number(value);
      return n.toLocaleString(undefined, { style: "currency", currency: "COP", maximumFractionDigits: 0 });
    } catch {
      return value;
    }
  }
//para la fecha formateada
  function formatDate(dateStr) {
    try {
      return new Date(dateStr).toLocaleDateString();
    } catch {
      return dateStr;
    }
  }

  // render fila de la tabla de historial
  function renderFilaPedido(p) {
    const tr = document.createElement("tr");
    tr.className = "hover:bg-gray-50";
    tr.innerHTML = `
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${p.id_pedido ?? p.id_pedidos}</td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${p.nombre_bebida}</td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${p.cantidad} unidades</td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${formatDate(p.fecha_pedido)}</td>
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${p.nombre_cliente}</td>
      <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">${formatCurrency(p.total_venta)}</td>
    `;
    tbody.appendChild(tr);
  }

  // render ingresos por producto (lista lateral)
  function renderIngresosPorProducto(items) {
    ingresosPorProductoEl.innerHTML = ""; // limpiar
    if (!items || items.length === 0) {
      ingresosPorProductoEl.innerHTML = `<div class="text-sm text-gray-500">No hay ingresos registrados.</div>`;
      return;
    }
    items.forEach(it => {
      const row = document.createElement("div");
      row.className = "flex justify-between";
      // mostrar nombre y monto formateado muuy importante
      row.innerHTML = `<span>${it.nombre_bebida}</span><span class="text-green-600">${formatCurrency(it.total_ingresos ?? it.total_ingresos)}</span>`;
      ingresosPorProductoEl.appendChild(row);
    });
  }

  // fetch carga historial y llena la tabla + calcula totales
  async function cargarHistorial() {
    try {
      const res = await fetch(`${API_BASE}/historial`);
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Error al obtener historial: ${res.status} ${text}`);
      }
      const datosContables = await res.json();

      // limpiar tbody antes de render
      tbody.innerHTML = "";

      // totales
      let totalUnidades = 0;
      let totalIngresos = 0;

      datosContables.forEach(p => {
        renderFilaPedido(p);
        totalUnidades += Number(p.cantidad || 0);
        totalIngresos += Number(p.total_venta || 0);
      });

      totalUnidadesEl.textContent = totalUnidades;
      totalIngresosEl.textContent = formatCurrency(totalIngresos);

    } catch (err) {
      console.error(err);
      // esta linea para ver el error visualmente en caso de fallos
      tbody.innerHTML = `<tr><td colspan="6" class="text-center text-red-500 py-4">No se pudo cargar el historial.</td></tr>`;
    }
  }

  // cargar ingresos por producto
  async function cargarIngresosPorProducto() {
    try {
      const res = await fetch(`${API_BASE}/ingresos`);
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Error al obtener ingresos: ${res.status} ${text}`);
      }
      const ingresos = await res.json();
      renderIngresosPorProducto(ingresos);
    } catch (err) {
      console.error(err);
      ingresosPorProductoEl.innerHTML = `<div class="text-sm text-red-500">No se pudieron cargar ingresos por producto.</div>`;
    }
  }

  // inicializar todo
  async function init() {
    await Promise.all([cargarHistorial(), cargarIngresosPorProducto()]);
  }

  init();
});

//bloque para el grafico

document.addEventListener("DOMContentLoaded", async () => {
  const ctx = document.getElementById("graficoCervezas");

  try {
    // Llamar al backend
    const response = await fetch("http://127.0.0.1:8000/contabilidad/ingresos");
    const datos = await response.json();

    if (!Array.isArray(datos) || datos.length === 0) {
      console.warn(" No hay datos de ingresos disponibles");
      return;
    }

    //Convertir totales a número pq estan llegango es string
    const etiquetas = datos.map(item => item.nombre_bebida);
    const totales = datos.map(item => parseFloat(item.total_ingresos));

    // Calcular porcentaje
    const totalGeneral = totales.reduce((sum, val) => sum + val, 0);
    const porcentajes = totales.map(val => totalGeneral > 0 ? ((val / totalGeneral) * 100).toFixed(2) : 0);

    //gráfico de barras
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: etiquetas,
        datasets: [{
          label: "% del total de ingresos",
          data: porcentajes,
          backgroundColor: [
            "rgba(249, 115, 22, 0.8)",
            "rgba(34, 197, 94, 0.8)",
            "rgba(59, 130, 246, 0.8)",
            "rgba(244, 63, 94, 0.8)",
          ],
          borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: true,
            text: "Porcentaje de ventas por cerveza",
            color: "#374151",
            font: { size: 16 }
          },
          tooltip: {
            callbacks: {
              label: context => {
                const idx = context.dataIndex;
                const valor = totales[idx].toLocaleString("es-CO", { style: "currency", currency: "COP" });
                const porcentaje = porcentajes[idx];
                return `${valor} (${porcentaje}%)`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: value => `${value}%`
            },
            title: {
              display: true,
              text: "% del total",
              color: "#6b7280"
            }
          }
        }
      }
    });
  } catch (error) {
    console.error(" Error al cargar gráfico:", error);
  }
});
