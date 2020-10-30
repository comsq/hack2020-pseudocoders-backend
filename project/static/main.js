async function createTask(type) {
    const response = await fetch('/tasks/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ type })
    });

    return await response.json();
}

async function getTaskStatus(id) {
    const response = await fetch(`/tasks/${id}/`);

    return await response.json();
}

async function updateTaskStatus(id) {
    const result = await getTaskStatus(id);

    const element = document.getElementById(`task-${id}`);
    const estatus = element.getElementsByClassName('task-status')[0];
    const eticks = element.getElementsByClassName('task-ticks')[0];
    const eresult = element.getElementsByClassName('task-result')[0];

    estatus.innerHTML = result.task_status;
    eticks.innerHTML = Number(eticks.innerHTML) + 1;
    eresult.innerHTML = result.task_result;

    if (result.task_status === 'SUCCESS' || result.task_status === 'FAILURE') return;

    setTimeout(() => updateTaskStatus(result.task_id), 1000);
}

document.querySelectorAll('.button').forEach(item => {
    item.addEventListener('click', function () {
        (async () => {
            const result = await createTask(this.dataset.type);

            const tr = document.createElement('tr');
            tr.id = `task-${result.task_id}`;
            tr.innerHTML = `
                <td class="task-id">${result.task_id}</td>
                <td class="task-status">PENDING</td>
                <td class="task-ticks">0</td>
                <td class="task-result"></td>
            `;
            tasks.appendChild(tr);

            setTimeout(() => updateTaskStatus(result.task_id), 1000);
        })();
    });
});
