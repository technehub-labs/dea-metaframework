/**
 * Meta Framework Explorer — site.js
 * Renders the 7×7 ECF matrix with three scenarios and an interactive cell inspector.
 */

(async () => {
  'use strict';

  // ── ECF canonical data ─────────────────────────────────
  // Single source of truth: pages/assets/matrix-data.json (same-origin).
  // Extracted from the former inline constants per CR-ECF-006 / ADR-ECF-001
  // lineage; the JSON is what the portal consumes via the sync workflow, so
  // the standalone page and the portal can never drift.
  //
  // Fallback: if the fetch fails (offline, partial deploy), we render with
  // empty cells rather than crashing — axes still show, detail panel explains.
  const FALLBACK_DOMAINS = [
    { id: 1, key: 'governance', name: 'Governance & Existence',  shortName: 'Governance', color: 'var(--l1)' },
    { id: 2, key: 'strategy',   name: 'Strategy & Direction',    shortName: 'Strategy',   color: 'var(--l2)' },
    { id: 3, key: 'agency',     name: 'Agency & Organization',   shortName: 'Agency',     color: 'var(--l3)' },
    { id: 4, key: 'party',      name: 'Party & Relationship',    shortName: 'Party',      color: 'var(--l4)' },
    { id: 5, key: 'product',    name: 'Product & Value',         shortName: 'Product',    color: 'var(--l5)' },
    { id: 6, key: 'operations', name: 'Enablement & Operations', shortName: 'Enablement', color: 'var(--l6)' },
    { id: 7, key: 'finance',    name: 'Finance & Accounting',    shortName: 'Finance',    color: 'var(--l7)' },
  ];
  const FALLBACK_STAGES = [
    { id: 1, key: 'conceive', name: 'Conceive',  fullName: 'Conceive' },
    { id: 2, key: 'design',   name: 'Design',    fullName: 'Design' },
    { id: 3, key: 'build',    name: 'Build',     fullName: 'Build / Acquire' },
    { id: 4, key: 'activate', name: 'Activate',  fullName: 'Deploy / Activate' },
    { id: 5, key: 'operate',  name: 'Operate',   fullName: 'Operate / Deliver' },
    { id: 6, key: 'improve',  name: 'Improve',   fullName: 'Measure / Learn' },
    { id: 7, key: 'retire',   name: 'Retire',    fullName: 'Retire / Renew' },
  ];

  async function loadMatrixData() {
    try {
      const resp = await fetch('./assets/matrix-data.json', { cache: 'no-cache' });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      if (!Array.isArray(data.domains) || data.domains.length !== 7) throw new Error('domains shape');
      if (!Array.isArray(data.stages) || data.stages.length !== 7) throw new Error('stages shape');
      if (!data.scenarios || typeof data.scenarios !== 'object') throw new Error('scenarios shape');
      return data;
    } catch (e) {
      console.warn('[matrix] matrix-data.json unavailable, using axes-only fallback:', e);
      return {
        domains: FALLBACK_DOMAINS,
        stages: FALLBACK_STAGES,
        scenarios: {
          foundation: { name: 'Foundation', description: 'Canonical ECF cells (data unavailable offline).', cells: {} },
          telecom:    { name: 'Telecom',    description: 'Telecom scenario (data unavailable offline).',  cells: {} },
          digital:    { name: 'Digital Services', description: 'Digital services scenario (data unavailable offline).', cells: {} },
        },
      };
    }
  }

  const matrixData = await loadMatrixData();
  const DOMAINS = matrixData.domains;
  const STAGES = matrixData.stages;
  const SCENARIOS = matrixData.scenarios;

  // ── State ───────────────────────────────────────────────
  let activeScenario = 'foundation';
  let activeCellKey = null;

  // ── DOM refs ────────────────────────────────────────────
  const matrixBody = document.getElementById('matrixBody');
  const detailPanel = document.getElementById('detailPanel');
  const detailCoords = document.getElementById('detailCoords');
  const detailTitle = document.getElementById('detailTitle');
  const detailGlyph = document.getElementById('detailGlyph');
  const detailText = document.getElementById('detailText');
  const detailMetaList = document.getElementById('detailMetaList');
  const detailActors = document.getElementById('detailActors');
  const detailEntities = document.getElementById('detailEntities');
  const detailRepoLink = document.getElementById('detailRepoLink');
  const detailMetamodelLink = document.getElementById('detailMetamodelLink');
  const detailClose = document.getElementById('detailClose');

  // ── Build the matrix ────────────────────────────────────
  function buildMatrix() {
    matrixBody.innerHTML = '';
    DOMAINS.forEach(domain => {
      const row = document.createElement('tr');
      // Domain header cell
      const head = document.createElement('th');
      head.className = 'domain-head';
      head.style.setProperty('--domain-color', domain.color);
      head.scope = 'row';
      head.innerHTML = `
        <span class="domain-num">D${domain.id}</span>
        <span class="domain-name">${domain.shortName}</span>
      `;
      row.appendChild(head);

      // 7 stage cells
      STAGES.forEach(stage => {
        const cellKey = `${domain.key}.${stage.key}`;
        const cellData = SCENARIOS[activeScenario].cells[cellKey] || null;
        const td = document.createElement('td');
        td.className = 'cell';
        if (cellData && cellData.glyph === '★') td.classList.add('high-risk');
        td.dataset.cellKey = cellKey;
        td.dataset.domain = domain.id;
        td.dataset.stage = stage.id;

        if (cellData) {
          td.innerHTML = `
            <span class="cell-tag">${stage.fullName}</span>
            <span class="cell-text">${escapeHtml(cellData.text)}</span>
            <span class="cell-glyph ${cellData.glyph === '★' ? 'risk' : ''}">${cellData.glyph}</span>
          `;
        } else {
          td.innerHTML = `<span class="cell-text" style="color:var(--text-3)">—</span>`;
        }

        td.addEventListener('click', () => openDetail(domain, stage, cellData));
        row.appendChild(td);
      });

      matrixBody.appendChild(row);
    });
  }

  // ── Scenario selector wiring ────────────────────────────
  document.querySelectorAll('.layer-btn[data-scenario]').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.layer-btn[data-scenario]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeScenario = btn.dataset.scenario;
      activeCellKey = null;
      closeDetail();
      buildMatrix();
    });
  });

  // ── Detail panel ────────────────────────────────────────
  function openDetail(domain, stage, cellData) {
    // Mark active cell
    document.querySelectorAll('.cell').forEach(c => c.classList.remove('active'));
    const cellEl = document.querySelector(`[data-cell-key="${domain.key}.${stage.key}"]`);
    if (cellEl) cellEl.classList.add('active');

    detailCoords.textContent = `${domain.name} × ${stage.fullName}`;
    detailTitle.textContent = `${domain.shortName} × ${stage.name}`;
    detailText.textContent = cellData ? cellData.text : 'No content for this cell in the current scenario.';

    if (cellData) {
      detailGlyph.textContent = cellData.glyph;
      detailGlyph.className = 'detail-glyph' + (cellData.glyph === '★' ? ' risk' : '');
    } else {
      detailGlyph.textContent = '·';
      detailGlyph.className = 'detail-glyph';
    }

    // Meta list
    detailMetaList.innerHTML = '';
    addMetaRow('Cell ID', `${domain.key}-${stage.key}`);
    addMetaRow('Domain', `${domain.id}. ${domain.name}`);
    addMetaRow('Stage', `${stage.id}. ${stage.fullName}`);
    if (cellData && cellData.glyph === '★') {
      addMetaRow('Handoff', 'High-risk handoff — invest attention here');
    }

    // Actors
    detailActors.innerHTML = '';
    const actors = cellData?.actors || ['—'];
    actors.forEach(a => {
      const chip = document.createElement('span');
      chip.className = 'detail-actor-chip';
      chip.textContent = a;
      detailActors.appendChild(chip);
    });

    // Metamodel entities
    detailEntities.innerHTML = '';
    const entities = cellData?.metamodelEntities || ['BusinessCapability'];
    entities.forEach(name => {
      const dt = document.createElement('dt');
      dt.textContent = 'Layer 2 / 4 entity';
      const dd = document.createElement('dd');
      dd.innerHTML = `<code>${name}</code>`;
      detailEntities.appendChild(dt);
      detailEntities.appendChild(dd);
    });

    detailPanel.classList.remove('hidden');
  }

  function addMetaRow(label, value) {
    const dt = document.createElement('dt');
    dt.textContent = label;
    const dd = document.createElement('dd');
    dd.textContent = value;
    detailMetaList.appendChild(dt);
    detailMetaList.appendChild(dd);
  }

  function closeDetail() {
    detailPanel.classList.add('hidden');
    document.querySelectorAll('.cell').forEach(c => c.classList.remove('active'));
  }

  detailClose.addEventListener('click', closeDetail);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      closeDetail();
      closeLegend();
    }
  });

  // ── Legend panel ────────────────────────────────────────
  const legendPanel = document.getElementById('legendPanel');
  const legendToggle = document.getElementById('legendToggle');
  const legendClose = document.getElementById('legendClose');
  let legendOpen = false;

  function openLegend() {
    legendPanel.classList.remove('hidden');
    legendToggle.classList.add('hidden');
    legendOpen = true;
  }
  function closeLegend() {
    legendPanel.classList.add('hidden');
    legendToggle.classList.remove('hidden');
    legendOpen = false;
  }
  legendToggle.addEventListener('click', openLegend);
  legendClose.addEventListener('click', closeLegend);

  // ── Helpers ─────────────────────────────────────────────
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])
    );
  }

  // ── Initial render ──────────────────────────────────────
  buildMatrix();

  // ──────────────────────────────────────────────────────────
  // Scenario cell builders
  // ──────────────────────────────────────────────────────────
})();