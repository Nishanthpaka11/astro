/**
 * வ உ சி யின் உறவைத் தேடி — Frontend Application
 */

const RENDER_BACKEND_URL = 'https://astro-hqtv.onrender.com';
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE = isLocal ? 'http://localhost:5000/api' : RENDER_BACKEND_URL + '/api';

// ─── State ──────────────────────────────────────────────────────────────────
let _deleteTarget = null; // {type, id}
let _searchTimer = null;

// ─── South Indian Chart ─────────────────────────────────────────────────────
const ZODIAC_SHORT = ["Mesha","Rishabha","Mithuna","Karka","Simha","Kanya","Tula","Vrischika","Dhanus","Makara","Kumbha","Meena"];
const SOUTH_INDIAN_POSITIONS = {0:{row:0,col:1},1:{row:0,col:2},2:{row:0,col:3},3:{row:1,col:3},4:{row:2,col:3},5:{row:3,col:3},6:{row:3,col:2},7:{row:3,col:1},8:{row:3,col:0},9:{row:2,col:0},10:{row:1,col:0},11:{row:0,col:0}};
const MALEFIC = ['Ra','Ke','Sa'];

function renderChart(containerId, chartData, lagnaSignIndex) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';
    for (let row = 0; row < 4; row++) {
        for (let col = 0; col < 4; col++) {
            const cell = document.createElement('div');
            if ((row===1||row===2)&&(col===1||col===2)) { cell.className='chart-cell chart-cell--empty'; container.appendChild(cell); continue; }
            let signIndex = -1;
            for (const [idx, pos] of Object.entries(SOUTH_INDIAN_POSITIONS)) { if (pos.row===row&&pos.col===col) { signIndex=parseInt(idx); break; } }
            cell.className = 'chart-cell';
            if (signIndex >= 0) {
                const nameEl = document.createElement('div'); nameEl.className='chart-cell__name'; nameEl.textContent=ZODIAC_SHORT[signIndex]; cell.appendChild(nameEl);
                const planets = chartData[String(signIndex)] || [];
                if (lagnaSignIndex === signIndex) { const a=document.createElement('div'); a.className='chart-cell__planets chart-cell__planets--asc'; a.textContent='Asc'; cell.appendChild(a); }
                planets.forEach(p => { const s=document.createElement('span'); s.className=MALEFIC.includes(p)?'chart-cell__planets chart-cell__planets--malefic':'chart-cell__planets'; s.textContent=p+' '; cell.appendChild(s); });
            }
            container.appendChild(cell);
        }
    }
}

// ─── Helpers ────────────────────────────────────────────────────────────────
function setText(id, text) { const el=document.getElementById(id); if(el) el.textContent=text; }
function showError(msg) { const el=document.getElementById('errorMsg'); if(el){el.textContent=msg;el.classList.add('active');} }
function hideError() { const el=document.getElementById('errorMsg'); if(el) el.classList.remove('active'); }
function showSuccess(msg) { const el=document.getElementById('successMsg'); if(el){el.textContent=msg;el.classList.add('active'); setTimeout(()=>el.classList.remove('active'),5000);} }
function showLoading(show) { const l=document.getElementById('loading'),f=document.getElementById('profileForm')||document.getElementById('birthForm'); if(l)l.classList.toggle('active',show); if(f)f.style.display=show?'none':'block'; }
function formatDate(ds) { if(!ds) return '—'; const d=new Date(ds+'T00:00:00'); const m=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']; return `${d.getDate()} ${m[d.getMonth()]} ${d.getFullYear()}`; }
function getPlanetSymbolUnicode(n) { return {'Sun':'☉','Moon':'☽','Mars':'♂','Mercury':'☿','Jupiter':'♃','Venus':'♀','Saturn':'♄','Rahu':'☊','Ketu':'☋'}[n]||''; }
function getParams() { return new URLSearchParams(window.location.search); }

// ─── Form Page ──────────────────────────────────────────────────────────────
const FORM_FIELDS = ['fullName','gender','dob','birthTime','birthPlace','height','weight','maritalStatus','motherTongue','religion','caste','profileCreatedBy','highestQualification','collegeUniversity','occupation','companyName','annualIncome','currentCity','nativePlace','familyDeity'];
const API_FIELDS = ['full_name','gender','dob','birth_time','birth_place','height','weight','marital_status','mother_tongue','religion','caste','profile_created_by','highest_qualification','college_university','occupation','company_name','annual_income','current_city','native_place','family_deity'];

function initFormPage() {
    const params = getParams();
    const type = params.get('type') || 'bride';
    const editId = params.get('edit') || '';
    document.getElementById('profileType').value = type;
    document.getElementById('editId').value = editId;
    switchTab(type);
    if (editId) {
        document.getElementById('formLabel').textContent = 'EDIT PROFILE';
        document.getElementById('formTitle').textContent = 'Edit Profile';
        document.getElementById('submitBtnText').textContent = 'Update Profile';
        document.getElementById('profileTabs').style.display = 'none';
        loadEditData(type, editId);
    }
}

function switchTab(type) {
    document.getElementById('profileType').value = type;
    document.getElementById('tabBride').className = type==='bride' ? 'tab-btn tab-btn--active' : 'tab-btn';
    document.getElementById('tabGroom').className = type==='groom' ? 'tab-btn tab-btn--active' : 'tab-btn';
    document.getElementById('formCardTitle').textContent = type==='bride' ? 'Bride Details' : 'Groom Details';
    const g = document.getElementById('gender');
    if (g && !document.getElementById('editId').value) g.value = type==='bride' ? 'Female' : 'Male';
}

function loadEditData(type, id) {
    const url = type==='bride' ? `${API_BASE}/brides/${id}` : `${API_BASE}/grooms/${id}`;
    fetch(url).then(r=>r.json()).then(data => {
        if (!data.success || !data.record) { showError('Record not found'); return; }
        const rec = data.record;
        FORM_FIELDS.forEach((f, i) => {
            const el = document.getElementById(f);
            if (el) el.value = rec[API_FIELDS[i]] || '';
        });
    }).catch(() => showError('Failed to load profile'));
}

function getFormData() {
    const obj = {};
    FORM_FIELDS.forEach((f, i) => {
        const el = document.getElementById(f);
        obj[API_FIELDS[i]] = el ? el.value.trim() : '';
    });
    return obj;
}

function submitProfile() {
    const type = document.getElementById('profileType').value;
    const editId = document.getElementById('editId').value;
    const data = getFormData();
    if (!data.full_name || !data.dob || !data.birth_time || !data.birth_place) { showError('Please fill all required fields: Full Name, DOB, Time, Place'); return; }
    hideError();
    showLoading(true);
    const isEdit = !!editId;
    const endpoint = type==='bride' ? `${API_BASE}/brides` : `${API_BASE}/grooms`;
    const url = isEdit ? `${endpoint}/${editId}` : endpoint;
    const method = isEdit ? 'PUT' : 'POST';
    fetch(url, { method, headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) })
    .then(r=>r.json()).then(res => {
        showLoading(false);
        if (res.error) { showError(res.error); return; }
        const newId = res.bride_id || res.groom_id || editId;
        if (res.chart && !isEdit) {
            sessionStorage.setItem('brideChart', JSON.stringify(res.chart));
            sessionStorage.setItem('lastProfileId', newId);
            sessionStorage.setItem('lastProfileType', type);
        }
        window.location.href = type==='bride' ? 'brides.html' : 'grooms.html';
    }).catch(() => { showLoading(false); showError('Connection error. Is the server running?'); });
}

// ─── Brides List ────────────────────────────────────────────────────────────
function loadBridesList(search) {
    const tbody = document.getElementById('bridesTableBody');
    if (!tbody) return;
    const q = search || '';
    fetch(`${API_BASE}/brides?search=${encodeURIComponent(q)}`)
    .then(r=>r.json()).then(data => {
        if (!data.success || !data.records || data.records.length===0) { tbody.innerHTML='<tr><td colspan="6" style="text-align:center;padding:40px;">No bride records found.</td></tr>'; return; }
        tbody.innerHTML = '';
        data.records.forEach(rec => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="font-weight:500;color:var(--gold);">${rec._id}</td>
                <td>${rec.full_name||'—'}</td>
                <td>${rec.dob ? formatDate(rec.dob) : '—'}</td>
                <td>${rec.birth_place||'—'}</td>
                <td>${[rec.religion,rec.caste].filter(Boolean).join(' / ')||'—'}</td>
                <td><div class="table-actions">
                    <button class="btn btn--secondary btn--sm" onclick="viewProfile('bride','${rec._id}')">View</button>
                    <a href="form.html?type=bride&edit=${rec._id}" class="btn btn--secondary btn--sm">Edit</a>
                    <button class="btn btn--danger btn--sm" onclick="openDeleteModal('bride','${rec._id}','${(rec.full_name||'').replace(/'/g,"\\'")}')">Delete</button>
                </div></td>`;
            tbody.appendChild(tr);
        });
    }).catch(() => { tbody.innerHTML='<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--error);">Failed to load records.</td></tr>'; });
}

function searchBrides() {
    clearTimeout(_searchTimer);
    _searchTimer = setTimeout(() => { loadBridesList(document.getElementById('brideSearch').value); }, 300);
}

// ─── Grooms List ────────────────────────────────────────────────────────────
function loadGroomsList(search) {
    const tbody = document.getElementById('groomsTableBody');
    if (!tbody) return;
    const q = search || '';
    fetch(`${API_BASE}/grooms?search=${encodeURIComponent(q)}`)
    .then(r=>r.json()).then(data => {
        if (!data.success || !data.records || data.records.length===0) { tbody.innerHTML='<tr><td colspan="6" style="text-align:center;padding:40px;">No groom records found.</td></tr>'; return; }
        tbody.innerHTML = '';
        data.records.forEach(rec => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="font-weight:500;color:var(--gold);">${rec._id}</td>
                <td>${rec.full_name||'—'}</td>
                <td>${rec.dob ? formatDate(rec.dob) : '—'}</td>
                <td>${rec.birth_place||'—'}</td>
                <td>${[rec.religion,rec.caste].filter(Boolean).join(' / ')||'—'}</td>
                <td><div class="table-actions">
                    <button class="btn btn--secondary btn--sm" onclick="viewProfile('groom','${rec._id}')">View</button>
                    <a href="form.html?type=groom&edit=${rec._id}" class="btn btn--secondary btn--sm">Edit</a>
                    <button class="btn btn--danger btn--sm" onclick="openDeleteModal('groom','${rec._id}','${(rec.full_name||'').replace(/'/g,"\\'")}')">Delete</button>
                </div></td>`;
            tbody.appendChild(tr);
        });
    }).catch(() => { tbody.innerHTML='<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--error);">Failed to load records.</td></tr>'; });
}

function searchGrooms() {
    clearTimeout(_searchTimer);
    _searchTimer = setTimeout(() => { loadGroomsList(document.getElementById('groomSearch').value); }, 300);
}

// ─── View Profile (redirect to results with chart) ──────────────────────────
function viewProfile(type, id) {
    const url = type==='bride' ? `${API_BASE}/brides/${id}` : `${API_BASE}/grooms/${id}`;
    fetch(url).then(r=>r.json()).then(data => {
        if (!data.success||!data.record) { alert('Record not found'); return; }
        const rec = data.record;
        if (rec.chart) {
            sessionStorage.setItem('brideChart', JSON.stringify(rec.chart));
            sessionStorage.removeItem('groomChart');
            sessionStorage.removeItem('porutham');
            window.location.href = 'results.html';
        } else { alert('No chart data available for this profile.'); }
    }).catch(() => alert('Failed to load profile.'));
}

// ─── Delete Modal ───────────────────────────────────────────────────────────
function openDeleteModal(type, id, name) {
    _deleteTarget = {type, id};
    const desc = document.getElementById('deleteModalDesc');
    if (desc) desc.textContent = `Are you sure you want to delete "${name}" (${id})? This action cannot be undone.`;
    document.getElementById('deleteModal').classList.add('active');
}

function closeDeleteModal() {
    _deleteTarget = null;
    document.getElementById('deleteModal').classList.remove('active');
}

function confirmDelete() {
    if (!_deleteTarget) return;
    const {type, id} = _deleteTarget;
    const url = type==='bride' ? `${API_BASE}/brides/${id}` : `${API_BASE}/grooms/${id}`;
    fetch(url, {method:'DELETE'}).then(r=>r.json()).then(res => {
        closeDeleteModal();
        if (res.success) {
            if (type==='bride') loadBridesList(); else loadGroomsList();
        } else { alert(res.error || 'Failed to delete'); }
    }).catch(() => { closeDeleteModal(); alert('Connection error.'); });
}

// ─── Match Page: Autocomplete Search ────────────────────────────────────────
function searchMatchBride(q) {
    if (!q || q.length < 1) { document.getElementById('brideAutoResults').classList.remove('active'); return; }
    fetch(`${API_BASE}/brides/search?q=${encodeURIComponent(q)}`).then(r=>r.json()).then(data => {
        renderAutoResults('brideAutoResults', data.results||[], 'bride');
    }).catch(()=>{});
}

function searchMatchGroom(q) {
    if (!q || q.length < 1) { document.getElementById('groomAutoResults').classList.remove('active'); return; }
    fetch(`${API_BASE}/grooms/search?q=${encodeURIComponent(q)}`).then(r=>r.json()).then(data => {
        renderAutoResults('groomAutoResults', data.results||[], 'groom');
    }).catch(()=>{});
}

function renderAutoResults(containerId, results, type) {
    const c = document.getElementById(containerId);
    if (!results.length) { c.innerHTML='<div class="autocomplete-item"><div class="autocomplete-item__name">No results found</div></div>'; c.classList.add('active'); return; }
    c.innerHTML = '';
    results.forEach(r => {
        const div = document.createElement('div');
        div.className = 'autocomplete-item';
        div.innerHTML = `<div class="autocomplete-item__id">${r._id}</div><div class="autocomplete-item__name">${r.full_name||'—'}</div><div class="autocomplete-item__meta">${r.dob ? formatDate(r.dob) : ''} · ${r.birth_place||''}</div>`;
        div.onclick = () => selectMatchProfile(type, r._id);
        c.appendChild(div);
    });
    c.classList.add('active');
}

function selectMatchProfile(type, id) {
    const url = type==='bride' ? `${API_BASE}/brides/${id}` : `${API_BASE}/grooms/${id}`;
    fetch(url).then(r=>r.json()).then(data => {
        if (!data.success||!data.record) return;
        const rec = data.record;
        if (type==='bride') {
            document.getElementById('selectedBrideId').value = id;
            document.getElementById('brideSearchInput').value = rec.full_name||id;
            renderProfilePreview('bridePreview', rec, '👰 BRIDE');
        } else {
            document.getElementById('selectedGroomId').value = id;
            document.getElementById('groomSearchInput').value = rec.full_name||id;
            renderProfilePreview('groomPreview', rec, '🤵 GROOM');
        }
        document.querySelectorAll('.autocomplete-results').forEach(el=>el.classList.remove('active'));
    }).catch(()=>{});
}

function renderProfilePreview(containerId, rec, label) {
    const c = document.getElementById(containerId);
    if (!c) return;
    const details = [
        ['ID', rec._id], ['DOB', rec.dob ? formatDate(rec.dob) : '—'],
        ['Place', rec.birth_place||'—'], ['Religion', rec.religion||'—'],
        ['Caste', rec.caste||'—'], ['Occupation', rec.occupation||'—'],
    ];
    c.className = 'profile-preview profile-preview--selected';
    c.innerHTML = `<div class="profile-preview__header"><div><div class="profile-preview__label">${label}</div><div class="profile-preview__name">${rec.full_name||'—'}</div></div></div>` +
        details.map(([l,v]) => `<div class="profile-preview__detail"><span class="profile-preview__detail-label">${l}</span><span class="profile-preview__detail-value">${v}</span></div>`).join('');
}

// ─── Run Match ──────────────────────────────────────────────────────────────
function runMatch() {
    const brideId = document.getElementById('selectedBrideId').value;
    const groomId = document.getElementById('selectedGroomId').value;
    if (!brideId || !groomId) { showError('Please select both a Bride and a Groom profile.'); return; }
    hideError();
    showLoading(true);
    fetch(`${API_BASE}/match`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({bride_id:brideId, groom_id:groomId}) })
    .then(r=>r.json()).then(data => {
        showLoading(false);
        if (data.error) { showError(data.error); return; }
        sessionStorage.setItem('brideChart', JSON.stringify(data.bride_chart));
        sessionStorage.setItem('groomChart', JSON.stringify(data.groom_chart));
        sessionStorage.setItem('porutham', JSON.stringify(data.porutham));
        if (data.match_id) sessionStorage.setItem('matchId', data.match_id);
        window.location.href = 'porutham.html';
    }).catch(() => { showLoading(false); showError('Connection error. Is the server running?'); });
}

// ─── Load Results Page ──────────────────────────────────────────────────────
function loadResults() {
    const brideData = sessionStorage.getItem('brideChart');
    const groomData = sessionStorage.getItem('groomChart');
    if (!brideData) return;
    const bride = JSON.parse(brideData);
    const groom = groomData ? JSON.parse(groomData) : null;
    displayChart(bride);
    const poruthamData = sessionStorage.getItem('porutham');
    if (poruthamData) { const btn=document.getElementById('viewPoruthamBtn'); if(btn) btn.style.display='inline-flex'; }
    if (groom) addChartSwitcher(bride, groom);
}

function displayChart(chart) {
    setText('resultTitle', `Birth Chart — ${chart.name}`);
    const metaEl = document.getElementById('resultMeta');
    if (metaEl) metaEl.textContent = `Born: ${formatDate(chart.dob)}, ${chart.time} · ${chart.place}`;
    setText('lagnaValue', chart.lagna.sign);
    setText('nakshatraValue', `${chart.nakshatra.name} – Pada ${chart.nakshatra.pada}`);
    setText('moonSignValue', chart.moon_sign.sign);
    setText('sunSignValue', chart.sun_sign.sign);
    renderChart('rasiChart', chart.rasi_chart, chart.lagna.sign_index);
    renderChart('navamsaChart', chart.navamsa_chart, chart.lagna.sign_index);
    const tbody = document.getElementById('planetTableBody');
    if (tbody) {
        tbody.innerHTML = '';
        chart.planets.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${getPlanetSymbolUnicode(p.name)} ${p.name}</td><td>${p.sign}</td><td>${p.degree}</td><td class="nakshatra">${p.nakshatra}</td><td>${p.pada}</td>`;
            tbody.appendChild(tr);
        });
    }
}

function addChartSwitcher(bride, groom) {
    const header = document.getElementById('resultsHeader');
    if (!header || document.getElementById('chartSwitcher')) return;
    const sw = document.createElement('div'); sw.id='chartSwitcher'; sw.style.cssText='display:flex;gap:12px;justify-content:center;margin-top:16px;';
    const bb = document.createElement('button'); bb.className='btn btn--primary'; bb.textContent=`👰 ${bride.name}`; bb.style.fontSize='13px';
    const gb = document.createElement('button'); gb.className='btn btn--secondary'; gb.textContent=`🤵 ${groom.name}`; gb.style.fontSize='13px';
    bb.onclick = () => { displayChart(bride); bb.className='btn btn--primary'; gb.className='btn btn--secondary'; };
    gb.onclick = () => { displayChart(groom); gb.className='btn btn--primary'; bb.className='btn btn--secondary'; };
    sw.appendChild(bb); sw.appendChild(gb); header.appendChild(sw);
}

// ─── Load Porutham Page ─────────────────────────────────────────────────────
function loadPorutham() {
    const data = sessionStorage.getItem('porutham');
    if (!data) return;
    const p = JSON.parse(data);
    setText('poruthamSubtitle', `${p.bride.name} & ${p.groom.name} — ${p.total}-Point Compatibility Check`);
    setText('scoreValue', `${p.score}/${p.total}`);
    const vt = document.getElementById('verdictTitle');
    if (vt) { vt.textContent = p.verdict; vt.className = `score-summary__title score-summary__title--${p.verdict_type}`; }
    const descs = {excellent:'An excellent match with strong compatibility across most factors.',good:'A good match with favorable compatibility.',average:'An average match. Consider consulting an astrologer.',poor:'Below average compatibility. Professional consultation recommended.'};
    setText('verdictDesc', descs[p.verdict_type]||'');
    const badge = document.getElementById('verdictBadge'), bt = document.getElementById('verdictBadgeText');
    if (badge && bt) { badge.style.display='inline-flex'; if(p.score>=6){badge.className='score-badge score-badge--good';bt.textContent='Recommended';}else{badge.className='score-badge score-badge--poor';bt.textContent='Consult Astrologer';} }
    const tbody = document.getElementById('poruthamTableBody');
    if (tbody) { tbody.innerHTML=''; p.results.forEach(item => { const tr=document.createElement('tr'); if(!item.matched)tr.className='row--no-match'; tr.innerHTML=`<td>${item.number}</td><td>${item.name}</td><td class="${item.matched?'status--match':'status--no-match'}">${item.matched?'✓ Match':'✗ No Match'}</td><td>${item.description}</td>`; tbody.appendChild(tr); }); }
}

// ─── Load History ───────────────────────────────────────────────────────────
function loadHistory() {
    const tbody = document.getElementById('historyTableBody');
    if (!tbody) return;
    fetch(`${API_BASE}/matches`).then(r=>r.json()).then(data => {
        if (!data.success || !data.records || data.records.length===0) { tbody.innerHTML='<tr><td colspan="7" style="text-align:center;padding:40px;">No match records found.</td></tr>'; return; }
        tbody.innerHTML = '';
        data.records.forEach(rec => {
            const tr = document.createElement('tr');
            const dateStr = rec.created_at ? new Date(rec.created_at).toLocaleDateString() : '—';
            const score = rec.porutham ? `${rec.porutham.score}/${rec.porutham.total}` : '—';
            const verdict = rec.porutham?.verdict || '—';
            tr.innerHTML = `
                <td style="font-weight:500;color:var(--gold);">${rec._id}</td>
                <td>${rec.bride_name||rec.bride_id||'—'}</td>
                <td>${rec.groom_name||rec.groom_id||'—'}</td>
                <td>${dateStr}</td><td>${score}</td><td>${verdict}</td>
                <td><button class="btn btn--secondary btn--sm" onclick="viewMatch('${rec._id}')">View</button></td>`;
            tbody.appendChild(tr);
        });
    }).catch(() => { tbody.innerHTML='<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--error);">Failed to load records.</td></tr>'; });
}

function viewMatch(matchId) {
    fetch(`${API_BASE}/matches/${matchId}`).then(r=>r.json()).then(data => {
        if (!data.success||!data.record) { alert('Record not found'); return; }
        const rec = data.record;
        sessionStorage.setItem('brideChart', JSON.stringify(rec.bride_chart));
        sessionStorage.setItem('groomChart', JSON.stringify(rec.groom_chart));
        sessionStorage.setItem('porutham', JSON.stringify(rec.porutham));
        sessionStorage.setItem('matchId', rec._id);
        window.location.href = 'porutham.html';
    }).catch(() => alert('Could not load this record.'));
}

// ─── PDF Download ───────────────────────────────────────────────────────────
function downloadPDF(elementId, filename) {
    const element = elementId==='body' ? document.body : document.getElementById(elementId);
    if (!element || typeof html2pdf === 'undefined') return;
    html2pdf().set({ margin:[10,5,10,5], filename, image:{type:'jpeg',quality:0.98}, html2canvas:{scale:2,useCORS:true,logging:false}, jsPDF:{unit:'mm',format:'a4',orientation:'portrait'}, pagebreak:{mode:['avoid-all','css','legacy'],avoid:['.chart-card','.summary-card','.score-section','.planet-table','.porutham-table','tr']} }).from(element).save().catch(()=>alert('Could not generate PDF.'));
}
