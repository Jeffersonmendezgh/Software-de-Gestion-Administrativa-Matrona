// auth.js
async function login(event) {
  event.preventDefault(); // evita que el form haga submit normal

  const body = {
    correo: document.getElementById("correoLogin").value,
    contrasena: document.getElementById("contrasenaLogin").value
  };

  // --- URL del endpoint de login: revisa en tu /docs cuál es ---
  // si tu router de auth usa prefix "/auth" usa "/auth/login"
  // si lo dejaste en "/usuarios" usa "/usuarios/login"
  // ejemplo:
  const LOGIN_URL = "http://127.0.0.1:8000/auth/login"; // <- ajustar si tu ruta es /usuarios/login

  try {
    const res = await fetch(LOGIN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Error en la petición" }));
      alert("Error: " + (err.detail ?? JSON.stringify(err)));
      return;
    }

    const data = await res.json();
    // guarda token (para pruebas está bien localStorage)
    localStorage.setItem("token", data.access_token);
    // redirigir al panel (ajusta ruta si tu template difiere)
    window.location.href = "/inventario";
  } catch (error) {
    console.error("Error fetch login:", error);
    alert("No se pudo conectar con el servidor");
  }
}

// helper para llamadas protegidas
async function fetchWithAuth(path, options = {}) {
  const token = localStorage.getItem("token");
  if (!options.headers) options.headers = {};
  options.headers["Authorization"] = `Bearer ${token}`;
  // asegúrate de usar URL completa o concatenar con tu host
  const base = "http://127.0.0.1:8000";
  return fetch(base + path, options);
}
