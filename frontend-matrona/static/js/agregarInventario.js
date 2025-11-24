document.addEventListener("DOMContentLoaded", () => {
    const btnGuardar = document.getElementById("btnGuardarProducto");

    // Detectar si es edición la ruta trae id_catalogo en la URL
    const urlParams = window.location.pathname.split("/"); //devuelve el otro pedazito de url es decir el numero para acceder al id
    const isEditing = urlParams.includes("editar-inventario");
    const editId = isEditing ? urlParams[urlParams.length - 1] : null;

    // Si es edición, traer datos actuales y rellenar form
    if (isEditing && editId) {
        fetch(`http://127.0.0.1:8000/catalogo/${editId}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById("nombre_cerveza").value = data.inventario.nombre_bebida;
                document.getElementById("descripcion").value = data.descripcion || "";
                document.getElementById("contenido").value = data.contenido || "";
                document.getElementById("alcohol").value = data.alcohol || "";
                document.getElementById("stock_inicial").value = data.inventario.cantidad_disponible;
                document.getElementById("precio_unidad").value = data.precio_unidad || "";
                document.getElementById("precio_sixpack").value = data.precio_sixpack || "";
                document.getElementById("precio_caja").value = data.precio_caja || "";
            });
    }
  //evento de click en el boton guardar con el objeto js que se va a enviar
    btnGuardar.addEventListener("click", async () => {
        const data = {
            nombre_bebida: document.getElementById("nombre_cerveza").value,
            descripcion: document.getElementById("descripcion").value,
            contenido: parseInt(document.getElementById("contenido").value),
            alcohol: document.getElementById("alcohol").value,
            cantidad_disponible: parseInt(document.getElementById("stock_inicial").value),
            unidades_agregadas: parseInt(document.getElementById("stock_inicial").value),
            precio_unidad: parseFloat(document.getElementById("precio_unidad").value),
            precio_sixpack: parseFloat(document.getElementById("precio_sixpack").value),
            precio_caja: parseFloat(document.getElementById("precio_caja").value)
        };

        console.log(" Enviando:", data);

        try {
            const response = await fetch(
                isEditing
                    ? `http://127.0.0.1:8000/catalogo/${editId}`   // PUT
                    : "http://127.0.0.1:8000/catalogo/",          // POST
                {
                    method: isEditing ? "PUT" : "POST",//si es edditing put sino post
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data) //object a json
                }
            );

            if (!response.ok) throw new Error(`Error ${response.status}`);

            const result = await response.json();
            console.log("Guardado:", result);

            alert(isEditing ? "Cerveza actualizada " : "Cerveza agregada ");

            window.location.href = "/inventario"; // volver al inventario
        } catch (error) {
            console.error(" Error:", error);
            alert("Hubo un error. Revisa la consola.");
        }
    });
});
