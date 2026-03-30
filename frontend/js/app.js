/**
 * வ உ சி யின் உறவைத் தேடி — Frontend Application
 * Handles form submission, API calls, chart rendering, and page navigation.
 */
// ─── API Configuration ──────────────────────────────────────────────────────
// IMPORTANT: After deploying to Render, replace this URL with your Render URL
// Example: 'https://your-app-name.onrender.com/api'
const RENDER_BACKEND_URL = 'https://YOUR-RENDER-APP.onrender.com';

// Auto-detect: if running on localhost, use localhost; otherwise use Render
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE = isLocal ? window.location.origin + '/api' : RENDER_BACKEND_URL + '/api';

// ─── South Indian Chart Layout ──────────────────────────────────────────────

const ZODIAC_SHORT = [
    "Mesha", "Rishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrischika",
    "Dhanus", "Makara", "Kumbha", "Meena"
];

/**
 * South Indian chart cell positions (row, col) for each sign index.
 */
const SOUTH_INDIAN_POSITIONS = {
    0:  { row: 0, col: 1 },  // Mesha
    1:  { row: 0, col: 2 },  // Rishabha
    2:  { row: 0, col: 3 },  // Mithuna
    3:  { row: 1, col: 3 },  // Karka
    4:  { row: 2, col: 3 },  // Simha
    5:  { row: 3, col: 3 },  // Kanya
    6:  { row: 3, col: 2 },  // Tula
    7:  { row: 3, col: 1 },  // Vrischika
    8:  { row: 3, col: 0 },  // Dhanus
    9:  { row: 2, col: 0 },  // Makara
    10: { row: 1, col: 0 },  // Kumbha
    11: { row: 0, col: 0 },  // Meena
};

// Malefic planets (show in red)
const MALEFIC = ['Ra', 'Ke', 'Sa'];

/**
 * Render a South Indian chart into a container element.
 */
function renderChart(containerId, chartData, lagnaSignIndex) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';

    // Create 4x4 grid
    for (let row = 0; row < 4; row++) {
        for (let col = 0; col < 4; col++) {
            const cell = document.createElement('div');

            // Check if this is a center cell (empty in South Indian format)
            if ((row === 1 || row === 2) && (col === 1 || col === 2)) {
                cell.className = 'chart-cell chart-cell--empty';
                container.appendChild(cell);
                continue;
            }

            // Find which sign goes here
            let signIndex = -1;
            for (const [idx, pos] of Object.entries(SOUTH_INDIAN_POSITIONS)) {
                if (pos.row === row && pos.col === col) {
                    signIndex = parseInt(idx);
                    break;
                }
            }

            cell.className = 'chart-cell';

            if (signIndex >= 0) {
                // Sign name
                const nameEl = document.createElement('div');
                nameEl.className = 'chart-cell__name';
                nameEl.textContent = ZODIAC_SHORT[signIndex];
                cell.appendChild(nameEl);

                // Planets in this house
                const planets = chartData[String(signIndex)] || [];

                // Check if this is the ascendant
                if (lagnaSignIndex === signIndex) {
                    const ascEl = document.createElement('div');
                    ascEl.className = 'chart-cell__planets chart-cell__planets--asc';
                    ascEl.textContent = 'Asc';
                    cell.appendChild(ascEl);
                }

                if (planets.length > 0) {
                    planets.forEach(p => {
                        const pEl = document.createElement('span');
                        if (MALEFIC.includes(p)) {
                            pEl.className = 'chart-cell__planets chart-cell__planets--malefic';
                        } else {
                            pEl.className = 'chart-cell__planets';
                        }
                        pEl.textContent = p + ' ';
                        cell.appendChild(pEl);
                    });
                }
            }

            container.appendChild(cell);
        }
    }
}


// ─── Form Submission ────────────────────────────────────────────────────────

function generateHoroscope() {
    const brideName = document.getElementById('brideName')?.value?.trim();
    const brideDob = document.getElementById('brideDob')?.value;
    const brideTime = document.getElementById('brideTime')?.value;
    const bridePlace = document.getElementById('bridePlace')?.value?.trim();
    const groomName = document.getElementById('groomName')?.value?.trim();
    const groomDob = document.getElementById('groomDob')?.value;
    const groomTime = document.getElementById('groomTime')?.value;
    const groomPlace = document.getElementById('groomPlace')?.value?.trim();

    // Optional fields
    const brideHeight = document.getElementById('brideHeight')?.value?.trim() || '';
    const brideWeight = document.getElementById('brideWeight')?.value?.trim() || '';
    const brideSalary = document.getElementById('brideSalary')?.value?.trim() || '';
    const groomHeight = document.getElementById('groomHeight')?.value?.trim() || '';
    const groomWeight = document.getElementById('groomWeight')?.value?.trim() || '';
    const groomSalary = document.getElementById('groomSalary')?.value?.trim() || '';

    // Validate required fields
    if (!brideName || !brideDob || !brideTime || !bridePlace ||
        !groomName || !groomDob || !groomTime || !groomPlace) {
        showError(t('error_fill_all'));
        return;
    }

    hideError();
    showLoading(true);

    const payload = {
        bride: {
            name: brideName, dob: brideDob, time: brideTime, place: bridePlace,
            height: brideHeight, weight: brideWeight, salary: brideSalary
        },
        groom: {
            name: groomName, dob: groomDob, time: groomTime, place: groomPlace,
            height: groomHeight, weight: groomWeight, salary: groomSalary
        }
    };

    fetch(`${API_BASE}/match`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        showLoading(false);

        if (data.error) {
            showError(data.error);
            return;
        }

        // Store results in sessionStorage
        sessionStorage.setItem('brideChart', JSON.stringify(data.bride_chart));
        sessionStorage.setItem('groomChart', JSON.stringify(data.groom_chart));
        sessionStorage.setItem('porutham', JSON.stringify(data.porutham));
        if (data.customer_id) {
            sessionStorage.setItem('customerId', data.customer_id);
        }

        // Navigate to results page (showing bride chart first)
        window.location.href = 'results.html';
    })
    .catch(err => {
        showLoading(false);
        showError('Connection error. Please make sure the server is running on localhost:5000.');
        console.error(err);
    });
}


// ─── Load Results Page ──────────────────────────────────────────────────────

function loadResults() {
    const brideData = sessionStorage.getItem('brideChart');
    const groomData = sessionStorage.getItem('groomChart');

    if (!brideData) {
        return;
    }

    const bride = JSON.parse(brideData);
    const groom = groomData ? JSON.parse(groomData) : null;

    // Default: show bride chart
    displayChart(bride);

    // Show "View Porutham" button if we have matching data
    const poruthamData = sessionStorage.getItem('porutham');
    if (poruthamData) {
        const btn = document.getElementById('viewPoruthamBtn');
        if (btn) btn.style.display = 'inline-flex';
    }

    // Add person switcher if both charts exist
    if (groom) {
        addChartSwitcher(bride, groom);
    }
}

function displayChart(chart) {
    // Title
    const titleEl = document.getElementById('resultTitle');
    if (titleEl) titleEl.textContent = `${t('results_title')} — ${chart.name}`;

    // Meta
    const metaEl = document.getElementById('resultMeta');
    if (metaEl) {
        const dobFormatted = formatDate(chart.dob);
        metaEl.textContent = `Born: ${dobFormatted}, ${chart.time} · ${chart.place}`;
    }

    // Summary Cards
    setText('lagnaValue', chart.lagna.sign);
    setText('nakshatraValue', `${chart.nakshatra.name} – Pada ${chart.nakshatra.pada}`);
    setText('moonSignValue', chart.moon_sign.sign);
    setText('sunSignValue', chart.sun_sign.sign);

    // Rasi Chart
    renderChart('rasiChart', chart.rasi_chart, chart.lagna.sign_index);

    // Navamsa Chart
    renderChart('navamsaChart', chart.navamsa_chart, chart.lagna.sign_index);

    // Planetary Table
    const tbody = document.getElementById('planetTableBody');
    if (tbody) {
        tbody.innerHTML = '';
        chart.planets.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${getPlanetSymbolUnicode(p.name)} ${p.name}</td>
                <td>${p.sign}</td>
                <td>${p.degree}</td>
                <td class="nakshatra">${p.nakshatra}</td>
                <td>${p.pada}</td>
            `;
            tbody.appendChild(tr);
        });
    }
}

function addChartSwitcher(bride, groom) {
    const header = document.getElementById('resultsHeader');
    if (!header) return;

    // Check if switcher already exists
    if (document.getElementById('chartSwitcher')) return;

    const switcher = document.createElement('div');
    switcher.id = 'chartSwitcher';
    switcher.style.cssText = 'display:flex;gap:12px;justify-content:center;margin-top:16px;';

    const brideBtn = document.createElement('button');
    brideBtn.className = 'btn btn--primary';
    brideBtn.textContent = `👰 ${bride.name}`;
    brideBtn.style.fontSize = '13px';
    brideBtn.onclick = () => {
        displayChart(bride);
        brideBtn.className = 'btn btn--primary';
        groomBtn.className = 'btn btn--secondary';
    };

    const groomBtn = document.createElement('button');
    groomBtn.className = 'btn btn--secondary';
    groomBtn.textContent = `🤵 ${groom.name}`;
    groomBtn.style.fontSize = '13px';
    groomBtn.onclick = () => {
        displayChart(groom);
        groomBtn.className = 'btn btn--primary';
        brideBtn.className = 'btn btn--secondary';
    };

    switcher.appendChild(brideBtn);
    switcher.appendChild(groomBtn);
    header.appendChild(switcher);
}


// ─── Load Porutham Page ─────────────────────────────────────────────────────

function loadPorutham() {
    const data = sessionStorage.getItem('porutham');
    if (!data) return;

    const porutham = JSON.parse(data);

    // Subtitle
    setText('poruthamSubtitle',
        `${porutham.bride.name} & ${porutham.groom.name} — ${porutham.total}-Point Compatibility Check`);

    // Score
    setText('scoreValue', `${porutham.score}/${porutham.total}`);

    // Verdict
    const verdictTitle = document.getElementById('verdictTitle');
    if (verdictTitle) {
        const verdictKey = `verdict_${porutham.verdict_type}`;
        verdictTitle.textContent = t(verdictKey) || porutham.verdict;
        verdictTitle.className = `score-summary__title score-summary__title--${porutham.verdict_type}`;
    }

    // Description
    const descKey = `verdict_${porutham.verdict_type}_desc`;
    setText('verdictDesc', t(descKey));

    // Badge
    const badge = document.getElementById('verdictBadge');
    const badgeText = document.getElementById('verdictBadgeText');
    if (badge && badgeText) {
        if (porutham.score >= 6) {
            badge.style.display = 'inline-flex';
            badge.className = 'score-badge score-badge--good';
            badgeText.textContent = t('badge_recommended');
        } else {
            badge.style.display = 'inline-flex';
            badge.className = 'score-badge score-badge--poor';
            badgeText.textContent = t('badge_consult');
        }
    }

    // Porutham Table
    const tbody = document.getElementById('poruthamTableBody');
    if (tbody) {
        tbody.innerHTML = '';
        porutham.results.forEach(item => {
            const tr = document.createElement('tr');
            if (!item.matched) tr.className = 'row--no-match';
            tr.innerHTML = `
                <td>${item.number}</td>
                <td>${item.name}</td>
                <td class="${item.matched ? 'status--match' : 'status--no-match'}">
                    ${item.matched ? t('match_yes') : t('match_no')}
                </td>
                <td>${item.description}</td>
            `;
            tbody.appendChild(tr);
        });
    }
}


// ─── Load History Page ──────────────────────────────────────────────────────

function loadHistory() {
    const tbody = document.getElementById('historyTableBody');
    if (!tbody) return;

    fetch(`${API_BASE}/customers`)
        .then(res => res.json())
        .then(data => {
            if (!data.success || !data.records || data.records.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:40px;" data-i18n="no_records">${t('no_records')}</td></tr>`;
                return;
            }

            tbody.innerHTML = '';
            data.records.forEach(rec => {
                const tr = document.createElement('tr');
                const dateStr = rec.created_at ? new Date(rec.created_at).toLocaleDateString() : '—';
                const score = rec.porutham ? `${rec.porutham.score}/${rec.porutham.total}` : '—';
                tr.innerHTML = `
                    <td style="font-weight:500;color:var(--gold);">${rec._id}</td>
                    <td>${rec.bride?.name || '—'}</td>
                    <td>${rec.groom?.name || '—'}</td>
                    <td>${dateStr}</td>
                    <td>${score}</td>
                    <td>
                        <button class="btn btn--primary" onclick="viewCustomer('${rec._id}')">
                            ${t('btn_view')}
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(err => {
            console.error('Failed to load history:', err);
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--error);">Failed to load records. Is MongoDB running?</td></tr>`;
        });
}

function viewCustomer(customerId) {
    fetch(`${API_BASE}/customers/${customerId}`)
        .then(res => res.json())
        .then(data => {
            if (!data.success || !data.record) {
                alert('Record not found');
                return;
            }

            const rec = data.record;

            // Store in session and navigate
            sessionStorage.setItem('brideChart', JSON.stringify(rec.bride_chart));
            sessionStorage.setItem('groomChart', JSON.stringify(rec.groom_chart));
            sessionStorage.setItem('porutham', JSON.stringify(rec.porutham));
            sessionStorage.setItem('customerId', rec._id);

            window.location.href = 'results.html';
        })
        .catch(err => {
            console.error('Failed to load customer:', err);
            alert('Could not load this record.');
        });
}


// ─── Helpers ────────────────────────────────────────────────────────────────

function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

function showError(msg) {
    const el = document.getElementById('errorMsg');
    if (el) {
        el.textContent = msg;
        el.classList.add('active');
    }
}

function hideError() {
    const el = document.getElementById('errorMsg');
    if (el) el.classList.remove('active');
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    const form = document.getElementById('birthForm');
    if (loading) loading.classList.toggle('active', show);
    if (form) form.style.display = show ? 'none' : 'block';
}

function formatDate(dateStr) {
    const d = new Date(dateStr + 'T00:00:00');
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`;
}

function getPlanetSymbolUnicode(name) {
    const symbols = {
        'Sun': '☉', 'Moon': '☽', 'Mars': '♂', 'Mercury': '☿',
        'Jupiter': '♃', 'Venus': '♀', 'Saturn': '♄',
        'Rahu': '☊', 'Ketu': '☋'
    };
    return symbols[name] || '';
}

/**
 * Downloads a specific element as a PDF using html2pdf.js
 * Captures full page content across multiple A4 pages.
 */
function downloadPDF(elementId, filename) {
    const element = elementId === 'body' ? document.body : document.getElementById(elementId);
    if (!element) return;

    // Configuration for html2pdf — multi-page support
    const opt = {
        margin: [10, 5, 10, 5],
        filename: filename,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            logging: false,
            letterRendering: true,
            scrollX: 0,
            scrollY: 0,
            windowWidth: document.documentElement.scrollWidth,
            windowHeight: document.documentElement.scrollHeight
        },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'], avoid: ['.chart-card', '.summary-card', '.score-section', '.planet-table', '.porutham-table', 'tr'] }
    };

    // Run html2pdf
    html2pdf().set(opt).from(element).save()
        .then(() => {
            console.log('PDF download initiated');
        })
        .catch(err => {
            console.error('PDF error:', err);
            alert('Could not generate PDF. Please try again.');
        });
}
