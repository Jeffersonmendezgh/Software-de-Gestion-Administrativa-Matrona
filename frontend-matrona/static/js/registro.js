// static/js/registro.js

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formRegistro");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // Evita que el navegador haga un POST "normal"

        // Capturar valores de los inputs
        const nombre = document.getElementById("nombre").value;
        const apellido = document.getElementById("apellidos").value;
        const correo = document.getElementById("correo").value;
        const direccion = document.getElementById("direccion").value;
        const contrasena = document.getElementById("contraseña").value;
        const rol = document.getElementById("rol").value;

        // Construir el objeto para enviar al backend
        const body = {
            nombre: nombre,
            apellido: apellido,
            correo: correo,
            direccion: direccion,   // 👈 añadido
            contrasena: contrasena,
            id_rol: rol             // aquí depende: ¿guardas rol como string o id en la BD?
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/usuarios/registro", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                const error = await response.json();
                alert("Error: " + error.detail);
                return;
            }

            const data = await response.json();
            alert("✅ Usuario registrado con éxito");
            console.log(data);

            // Redirigir después de registrar
            window.location.href = "index.html"; 
        } catch (err) {
            console.error("Error en la solicitud:", err);
            alert("Error al conectar con el servidor");
        }
    });
});
