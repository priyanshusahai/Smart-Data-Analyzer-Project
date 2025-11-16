document.getElementById("analyzeForm").addEventListener("submit", async function (event) {
    event.preventDefault(); 

    const form = document.getElementById("analyzeForm");
    const formData = new FormData(form);

    document.getElementById("result").innerHTML = "Analyzing... Please wait ⏳";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById("result").innerHTML = `<span style="color:red;">${data.error}</span>`;
            return;
        }

        // Show message + Open Report Button
        document.getElementById("result").innerHTML = `
            <p><strong>${data.message}</strong></p>
            <a href="${data.report}" target="_blank">
                <button class="submit-btn">Open Report</button>
            </a>
        `;
    } catch (err) {
        document.getElementById("result").innerHTML = "Something went wrong!";
    }
});
