// script.js
emailjs.init("-nTJOuE5kObbc5OVs"); // Reemplaza "YOUR_USER_ID" con tu ID de EmailJS

document.getElementById('drawButton').addEventListener('click', async function () {
    const participantsText = document.getElementById('participants').value;
    const participants = participantsText.split('\n').filter(email => email.trim() !== '');

    if (participants.length < 2) {
        alert('Necesitas al menos 2 participantes para el sorteo.');
        return;
    }

    const shuffled = participants.sort(() => Math.random() - 0.5);
    const thief = shuffled[0];
    const police = shuffled[1];

    document.getElementById('status').textContent = 'Enviando resultados...';

    try {
        // Enviar correos
        await sendEmail(thief, "Ladrón");
        await sendEmail(police, "Policía");

        document.getElementById('status').textContent = 'Resultados enviados con éxito.';
    } catch (error) {
        document.getElementById('status').textContent = 'Error al enviar los correos.';
        console.error(error);
    }
});

async function sendEmail(email, role) {
    return emailjs.send("service_lj1tdkf", "template_wafqs24", {
        to_email: email,
        role: role,
    });
}
