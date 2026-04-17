document.addEventListener('DOMContentLoaded', () => {

//sidebar y funcion para ocultar
const sidebar = document.getElementById("sidebar");
const verSidebar = document.getElementById("verSidebar");

//ocultar el sidebar al hacer click afuera
document.addEventListener('click', (e) => {
    const clickedOutside = !sidebar.contains(e.target) && !verSidebar.contains(e.target);
    const esBotonOLink = e.target.closest('button, a, i'); //closest para buscar ancestro más cercano de un elemento que coincide con un selector CSS específico
    const isVisible = !sidebar.classList.contains('hidden');
//containts verifica si sidebar es un descendiente de un evento.target el DOM, necesito recordarlo 
    if (clickedOutside && !esBotonOLink && isVisible) {
        sidebar.classList.add('-translate-x-full');
        verSidebar.classList.remove('-translate-x-full')
    }
});

//mostrar el sidebar al hacer click en el boton que tengo oculto
verSidebar.addEventListener('click', () => {
    sidebar.classList.remove('-translate-x-full');
    verSidebar.classList.add('-translate-x-full');
});
})