// =========================
// Helper: decodificar JWT
// =========================
function parseJwt(token) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    console.error("Error parseando JWT:", e);
    return null;
  }
}

// =========================
// Login
// =========================
async function login(event) {
  event.preventDefault();

  const body = {
    correo: document.getElementById("correoLogin").value,
    contrasena: document.getElementById("contrasenaLogin").value,
  };

  const LOGIN_URL = "http://127.0.0.1:8000/auth/login";

  try {
    const res = await fetch(LOGIN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Error en la petición" }));
      alert("Error: " + (err.detail ?? JSON.stringify(err)));
      return;
    }

    const data = await res.json();
    // Guardar token en localStorage
    localStorage.setItem("token", data.access_token);

    // Decodificar token
    const decoded = parseJwt(data.access_token);
    console.log("Token decodificado:", decoded);

    if (decoded && decoded.role) {
      switch (decoded.role) {
        case "1": // Administrador
          window.location.href = "/menu";
          break;
        case "2": // Empleado
          window.location.href = "/inventario";
          break;
        case "3": // Cliente
          window.location.href = "/catalogo";
          break;
        default:
          alert("Rol desconocido, no se pudo redirigir.");
      }
    } else {
      alert("Error: no se pudo obtener el rol del token");
    }
  } catch (error) {
    console.error("Error fetch login:", error);
    alert("No se pudo conectar con el servidor");
  }
}

// =========================
// Helper para llamadas protegidas
// =========================
async function fetchWithAuth(path, options = {}) {
  const token = localStorage.getItem("token");
  if (!options.headers) options.headers = {};
  options.headers["Authorization"] = `Bearer ${token}`;
  const base = "http://127.0.0.1:8000";
  return fetch(base + path, options);
}
