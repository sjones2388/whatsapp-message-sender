document.getElementById('uploadBtn').addEventListener('click', () => {
    const fileInput = document.getElementById('file').files[0];
    const formData = new FormData();
    formData.append('file', fileInput);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
        } else {
            alert(data.message);
            console.log(data.filepath);
        }
    });
});

document.getElementById('devicesBtn').addEventListener('click', () => {
    fetch('/devices')
        .then(response => response.json())
        .then(data => {
            const deviceList = document.getElementById('deviceList');
            if (data.error) {
                deviceList.innerHTML = `<p class="text-danger">${data.error}</p>`;
            } else {
                deviceList.innerHTML = `<p>Dispositivos: ${data.devices.join(', ')}</p>`;
            }
        });
});

document.getElementById('sendBtn').addEventListener('click', () => {
    const messageTemplate = document.getElementById('message').value;
    const devices = ["device1", "device2"]; // Aquí puedes usar la lógica para obtener dispositivos seleccionados
    const filepath = "ruta/a/tu/archivo.xlsx"; // Cambiar dinámicamente si es necesario

    fetch('/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filepath, message_template: messageTemplate, devices })
    })
    .then(response => response.json())
    .then(data => {
        const logs = document.getElementById('logs');
        if (data.error) {
            logs.innerHTML = `<p class="text-danger">${data.error}</p>`;
        } else {
            logs.innerHTML = `<p class="text-success">${data.message}</p>`;
        }
    });
});
