let data = {};

async function loadData() {
    try {
        const response = await fetch("/api/status");

        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }

        data = await response.json();

        getTH();
        getTD();
    } catch (err) {
        console.error(err);
    }
}


function getTH() {
   const head = document.querySelector("thead");
   if (!data || Object.keys(data).length === 0) {
      head.innerHTML = "";
      return;
   }

   const firstDevice = Object.values(data)[0] || {};
   const columns = ["Device", ...Object.keys(firstDevice)];

   let html = "<tr>";
   for (const col of columns) {
      html += `<th>${col}</th>`;
   }
   html += "</tr>";

   head.innerHTML = html;
}


loadData();

function getTD() {
    const body = document.querySelector("tbody");
    if (!data || Object.keys(data).length === 0) {
        body.innerHTML = "";
        return;
    }
    const firstDevice = Object.values(data)[0] || {};
    const columns = ["Device", ...Object.keys(firstDevice)];
    let html = "";
    for (const [deviceName, info] of Object.entries(data)) {
        html += "<tr>";
        for (const col of columns) {
            let value;
            if (col === "Device") {
                value = deviceName;
            } else if (col === "state") {
                const state = info.state ? "on" : "off";
                value = `<span class="status-dot ${state}"></span>${info.state ? "Online" : "Offline"}`;
            } else {
                value = info[col] ?? "";
            }
            html += `<td>${value}</td>`;
        }
        html += "</tr>";
    }
    body.innerHTML = html;
}

setInterval(loadData, 5000);