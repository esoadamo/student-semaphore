/**
 * @typedef {{name: string, status: string | null}} ComputerStatus
 * @typedef {(ComputerStatus | null)[][]} RoomLayout
 */

/**
 * Load the room layout from a predefined configuration
 * @param roomId {string}
 * @returns {Promise<RoomLayout>} The room layout
 */
async function fetchRoomStatus(roomId) {
    const response = await fetch(`api/room/${roomId}`);
    return response.json();
}

async function refreshRoomStatus(roomId, layoutElement) {
    const room = await fetchRoomStatus(roomId);
    layoutElement.innerHTML = '';
    room.forEach((row, rIndex) => {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('row');

        row.forEach((cell, cIndex) => {
            // create a wrapper so we can place the student name below the cell
            const cellWrapper = document.createElement('div');
            cellWrapper.classList.add('cell-wrapper');
            // mark position so we can fill names later
            cellWrapper.dataset.row = String(rIndex);
            cellWrapper.dataset.col = String(cIndex);

            const cellDiv = document.createElement('div');
            const nameDiv = document.createElement('div');
            nameDiv.classList.add('student-name');
            nameDiv.textContent = '';
            cellDiv.classList.add('cell');
            if (cell != null) {
                cellDiv.classList.add('computer');
                cellDiv.classList.add(`status-${cell.status}`);
                cellDiv.dataset.computer = JSON.stringify(cell);
                nameDiv.textContent = cell.name;
            }

            cellWrapper.appendChild(cellDiv);
            cellWrapper.appendChild(nameDiv);
            rowDiv.appendChild(cellWrapper);
        });

        layoutElement.appendChild(rowDiv);
    });
}

/**
 * Initialize the room layout
 * @param roomId {string}
 * @param layoutElement {HTMLElement}
 * @returns {Promise<number>}
 */
async function initRoom(roomId, layoutElement) {
    await refreshRoomStatus(roomId, layoutElement);
    return setInterval(() => refreshRoomStatus(roomId, layoutElement), 7000);
}
