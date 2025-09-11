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

    ROOM.forEach(row => {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('row');

        row.forEach(cell => {
            const cellDiv = document.createElement('div');
            cellDiv.classList.add('cell');
            if (cell === 'X') {
                cellDiv.classList.add('computer');
            }
            rowDiv.appendChild(cellDiv);
        });

        layout.appendChild(rowDiv);
    });
});