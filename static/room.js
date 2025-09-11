const ROOM = [
    ['X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X'],
    ['X', ' ', ' ', 'X'],
    ['X', ' ', ' ', 'X'],
    ['X', ' ', ' ', 'X'],
    ['X', ' ', ' ', 'X'],
    ['X', ' ', ' ', ' '],
]

window.addEventListener('load', async () => {
    const layout = document.getElementById('room-layout');

    ROOM.forEach((row, rIndex) => {
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
            cellDiv.classList.add('cell');
            if (cell === 'X') {
                cellDiv.classList.add('computer');
            }

            // student name element below the cell (initially empty)
            const nameDiv = document.createElement('div');
            nameDiv.classList.add('student-name');
            nameDiv.textContent = ''; // fill later with actual student names

            cellWrapper.appendChild(cellDiv);
            cellWrapper.appendChild(nameDiv);
            rowDiv.appendChild(cellWrapper);
        });

        layout.appendChild(rowDiv);
    });
});