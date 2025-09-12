/**
 * @typedef {{name: string, hostname: string | null, status: string | null}} ComputerStatus
 * @typedef {(ComputerStatus | null)[][]} RoomLayout
 */

/**
 * Load the room layout from a predefined configuration
 * @returns {Promise<RoomLayout>} The room layout
 */
async function fetchRoomStatus() {
    const response = await fetch(`api/room`);
    return response.json();
}

async function assignComputer(rowIndex, collIndex) {
    await fetch(`api/room/assign`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ row: rowIndex, col: collIndex })
    });
    await setComputerStatus('green');
}


async function setComputerStatus(status) {
    await fetch(`api/room/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status })
    });
}

async function refreshRoomStatus(hostname, layoutElement) {
    const room = await fetchRoomStatus();

    let computerSet = false;

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

                if (cell.hostname === hostname) {
                    cellDiv.classList.add('current');
                    computerSet = true;
                } else if (cell.hostname === null) {
                    cellDiv.classList.add('unassigned');
                    cellDiv.onclick = async () => {
                        await assignComputer(rIndex, cIndex);
                        await refreshRoomStatus(hostname, layoutElement);
                    }
                }
            }

            cellWrapper.appendChild(cellDiv);
            cellWrapper.appendChild(nameDiv);
            rowDiv.appendChild(cellWrapper);
        });

        layoutElement.appendChild(rowDiv);
    });

    if (computerSet) {
        // If the computer is set, then add a semaphore to the bottom
        // Semaphore will allow to select the state of the computer
        const semaphoreDiv = document.createElement('div');
        semaphoreDiv.classList.add('semaphore');
        const states = ['green', 'yellow', 'red'];
        states.forEach(state => {
            const stateDiv = document.createElement('div');
            stateDiv.classList.add('semaphore-state');
            stateDiv.classList.add(`status-${state}`);
            stateDiv.title = state.replace('-', ' ').toUpperCase();
            stateDiv.onclick = async () => {
                await setComputerStatus(state);
                await refreshRoomStatus(hostname, layoutElement);
            };
            semaphoreDiv.appendChild(stateDiv);
        });
        layoutElement.appendChild(semaphoreDiv);
    }
}

/**
 * Initialize the room layout
 * @param hostname {string}
 * @param layoutElement {HTMLElement}
 * @returns {Promise<number>}
 */
async function initRoom(hostname, layoutElement) {
    await setComputerStatus('green');
    await refreshRoomStatus(hostname, layoutElement);
    return setInterval(() => refreshRoomStatus(hostname, layoutElement), 7000);
}
