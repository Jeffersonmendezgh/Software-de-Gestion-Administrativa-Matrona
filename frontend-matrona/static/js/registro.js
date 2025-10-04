// static/js/registro.js
console.log("esta funcionando")
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formRegistro");
    
    form.addEventListener("submit", async (e) => {
        e.preventDefault(); 

        // Capturar valores de los inputs
        const nombre = document.getElementById("nombre").value;
        const apellido = document.getElementById("apellidos").value;
        const correo = document.getElementById("correo").value;
        const direccion = document.getElementById("direccion").value;
        const contrasena = document.getElementById("contrasena").value;
        const rol = document.getElementById("rol").value;

        // Construir el objeto para enviar al backend
        const body = {
            nombre: nombre,
            apellido: apellido,
            correo: correo,
            direccion: direccion,  
            contrasena: contrasena,
            id_rol: parseInt(rol)             
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/auth/registro", {
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
            alert("Te has registrado exitosamente Bienvenido a nuestro sistema ¡Matrona!");
            console.log(data);

            // Redirigir después de registrar
            
        } catch (err) {
            console.error("Error en la solicitud:", err);
            alert("Error al conectar con el servidor");
        }
    });
});
