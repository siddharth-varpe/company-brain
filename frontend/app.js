async function ask() {

    let q = document.getElementById("question").value;
    if (!q) return;

    let chat = document.getElementById("chat");

    chat.innerHTML += `<div class="msg user">You: ${q}</div>`;

    let res = await fetch(`http://127.0.0.1:8000/ask?question=${encodeURIComponent(q)}`);
    let data = await res.json();

    let evidenceHTML = "";
    if (data.evidence && data.evidence.length > 0) {
        evidenceHTML = "<br><b>Related work:</b><ul>";
        data.evidence.forEach(e => evidenceHTML += `<li>${e}</li>`);
        evidenceHTML += "</ul>";
    }

    chat.innerHTML += `
        <div class="msg bot">
        Expert: <b>${data.expert}</b><br>
        ${data.reason}
        ${evidenceHTML}
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;
    document.getElementById("question").value = "";
}
