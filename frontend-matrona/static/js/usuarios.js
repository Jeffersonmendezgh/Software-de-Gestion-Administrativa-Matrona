// Ejemplo: borrar usuario
async function eliminarUsuario(id) {
    const res = await fetchWithAuth(`/usuarios/${id}`, { method: "DELETE" });
    if (!res.ok) {
        alert("No tienes permisos o el token es inválido");
        return;
    }
    alert("Usuario eliminado correctamente");
}
