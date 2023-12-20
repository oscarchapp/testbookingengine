document.addEventListener("DOMContentLoaded", function() {
    let roomsData = JSON.parse(document.getElementById("roomsData").textContent);
    document.getElementById("searchForm").addEventListener("submit", function(event) {
        event.preventDefault();
        buscar();
    });

    function buscar() {
        let query = document.getElementById("searchInput").value.toLowerCase();
        let resultados = roomsData.filter(room => {
            let parts = room.name.toLowerCase().split('.');
            return parts.some(part => part.trim().startsWith(query.trim()));
        });
        mostrarResultados(resultados);
    }

    function mostrarResultados(resultados) {
        let resultsContainer = document.getElementById("results");
        let roomListContainer = document.getElementById("roomList");
        roomListContainer.style.display = "none";
        resultsContainer.innerHTML = "";
        if (resultados.length === 0) {
            resultsContainer.innerHTML = "No se encontraron resultados.";
        } else {
            resultados.forEach(room => {
                let roomDiv = document.createElement("div");
                roomDiv.classList.add("row", "card", "mt-3", "mb-3", "hover-card", "bg-tr-250");
                let colDiv = document.createElement("div");
                colDiv.classList.add("col", "p-3");
                let roomInfoDiv = document.createElement("div");
                roomInfoDiv.classList.add("room-info");
                roomInfoDiv.textContent = `${room.name} (${room.room_type__name})`;
                let detailsLinkDiv = document.createElement("div");
                detailsLinkDiv.classList.add("details-link");
                let detailsLink = document.createElement("a");
                detailsLink.href = "{% url 'room_details' pk=0 %}".replace('0', room.id);
                detailsLink.textContent = "Ver detalles";
                detailsLinkDiv.appendChild(detailsLink);
                colDiv.appendChild(roomInfoDiv);
                colDiv.appendChild(detailsLinkDiv);
                roomDiv.appendChild(colDiv);
                resultsContainer.appendChild(roomDiv);
            });
        }
        resultsContainer.style.display = "block";
    }
});