function toggleQuantumField() {
    const algorithm = document.getElementById('algorithm').value;
    const quantumField = document.getElementById('quantum-field');
    quantumField.style.display = algorithm === 'rr' ? 'block' : 'none';
}

function addProcess() {
    const table = document.getElementById('process-table').getElementsByTagName('tbody')[0];
    const rowCount = table.rows.length;
    const newRow = table.insertRow();
    
    newRow.innerHTML = `
        <td><input type="text" class="process-id" value="P${rowCount + 1}" required></td>
        <td><input type="number" class="arrival-time" min="0" value="0" required></td>
        <td><input type="number" class="burst-time" min="1" value="${Math.floor(Math.random() * 10) + 1}" required></td>
        <td><input type="number" class="priority" min="1" value="${Math.floor(Math.random() * 5) + 1}" required></td>
        <td><button class="remove-btn" onclick="removeProcess(this)">Remove</button></td>
    `;
}

function removeProcess(button) {
    const table = document.getElementById('process-table').getElementsByTagName('tbody')[0];
    if (table.rows.length > 1) {
        button.closest('tr').remove();
    } else {
        alert("You need at least one process!");
    }
}

function simulate() {
    const algorithm = document.getElementById('algorithm').value;
    const timeQuantum = algorithm === 'rr' ? parseInt(document.getElementById('time-quantum').value) : 2;
    
    const processRows = document.getElementById('process-table').getElementsByTagName('tbody')[0].rows;
    const processes = [];
    
    for (let i = 0; i < processRows.length; i++) {
        const row = processRows[i];
        processes.push({
            id: row.cells[0].getElementsByTagName('input')[0].value,
            arrival_time: parseInt(row.cells[1].getElementsByTagName('input')[0].value),
            burst_time: parseInt(row.cells[2].getElementsByTagName('input')[0].value),
            priority: parseInt(row.cells[3].getElementsByTagName('input')[0].value)
        });
    }
    
    fetch('/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            algorithm: algorithm,
            processes: processes,
            time_quantum: timeQuantum
        })
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during simulation.');
    });
}

function displayResults(data) {
    document.getElementById('results-section').style.display = 'block';
    renderGanttChart(data.gantt_chart);
    displayMetrics(data);
    displayProcessDetails(data);
}

function renderGanttChart(ganttData) {
    const ganttContainer = document.getElementById('gantt-chart');
    ganttContainer.innerHTML = '';
    
    let maxTime = 0;
    
    ganttData.forEach(item => {
        const duration = item.end - item.start;
        maxTime = Math.max(maxTime, item.end);
        
        const block = document.createElement('div');
        block.className = `gantt-block ${item.process === 'Idle' ? 'idle' : ''}`;
        block.style.width = `${duration * 30}px`;
        block.style.backgroundColor = getRandomColor(item.process);
        block.textContent = item.process;
        block.setAttribute('data-end', item.end);
        
        ganttContainer.appendChild(block);
    });
}

function getRandomColor(seed) {
    if (seed === 'Idle') return '#95a5a6';
    const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'];
    let hash = 0;
    for (let i = 0; i < seed.length; i++) {
        hash = seed.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
}

function displayMetrics(data) {
    const metricsContainer = document.getElementById('metrics-table');
    metricsContainer.innerHTML = `
        <div class="metric-item">
            <h4>Algorithm</h4>
            <p>${data.algorithm}</p>
        </div>
        <div class="metric-item">
            <h4>Average Waiting Time</h4>
            <p>${data.avg_waiting.toFixed(2)}</p>
        </div>
        <div class="metric-item">
            <h4>Average Turnaround Time</h4>
            <p>${data.avg_turnaround.toFixed(2)}</p>
        </div>
    `;
}

function displayProcessDetails(data) {
    const tableBody = document.getElementById('process-details-body');
    tableBody.innerHTML = '';
    
    data.processes.forEach((process, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${process.id}</td>
            <td>${process.arrival_time}</td>
            <td>${process.burst_time}</td>
            <td>${process.priority}</td>
            <td>${data.completion_times[index]}</td>
            <td>${data.turnaround_times[index]}</td>
            <td>${data.waiting_times[index]}</td>
        `;
        tableBody.appendChild(row);
    });
}