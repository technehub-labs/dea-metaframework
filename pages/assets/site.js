/**
 * Meta Framework Explorer — site.js
 * Renders the 7×7 ECF matrix with three scenarios and an interactive cell inspector.
 */

(async () => {
  'use strict';

  // ── ECF canonical data ─────────────────────────────────
  // The 7 domains (rows) — order is axiomatic: governance first, finance last.
  const DOMAINS = [
    { id: 1, key: 'governance', name: 'Governance & Existence', shortName: 'Governance', color: 'var(--l1)' },
    { id: 2, key: 'supply',     name: 'Supply & Resources',      shortName: 'Supply',     color: 'var(--l2)' },
    { id: 3, key: 'people',     name: 'People & Organization',  shortName: 'People',     color: 'var(--l3)' },
    { id: 4, key: 'customer',   name: 'Customer & Demand',      shortName: 'Customer',   color: 'var(--l4)' },
    { id: 5, key: 'product',    name: 'Product & Offering',     shortName: 'Product',    color: 'var(--l5)' },
    { id: 6, key: 'operations', name: 'Operations & Delivery',  shortName: 'Operations', color: 'var(--l6)' },
    { id: 7, key: 'finance',    name: 'Finance & Value',        shortName: 'Finance',    color: 'var(--l7)' },
  ];

  // The 7 stages (columns) — universal lifecycle order
  const STAGES = [
    { id: 1, key: 'conceive', name: 'Conceive',           fullName: 'Conceive' },
    { id: 2, key: 'design',   name: 'Design',             fullName: 'Design' },
    { id: 3, key: 'build',    name: 'Build',              fullName: 'Build / Acquire' },
    { id: 4, key: 'activate', name: 'Activate',           fullName: 'Deploy / Activate' },
    { id: 5, key: 'operate',  name: 'Operate',            fullName: 'Operate / Deliver' },
    { id: 6, key: 'improve',  name: 'Improve',            fullName: 'Measure / Learn' },
    { id: 7, key: 'retire',   name: 'Retire',             fullName: 'Retire / Renew' },
  ];

  // ── Cell content per scenario ───────────────────────────
  // Each cell has: text (description), glyph (●/★/·), actors (chip list),
  // metamodelEntities (linked entity types from dea-metamodel).
  const SCENARIOS = {
    foundation: {
      name: 'Foundation',
      description: 'Generic business object behavior — the canonical ECF cells.',
      cells: buildFoundationCells(),
    },
    telecom: {
      name: 'Telecom',
      description: 'A telecom operator — network attach, mediation, NOC, lawful intercept.',
      cells: buildTelecomCells(),
    },
    digital: {
      name: 'Digital Services',
      description: 'A digital services company — feature flags, FinOps, SRE, MRR.',
      cells: buildDigitalCells(),
    },
  };

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
  function buildFoundationCells() {
    return {
      // Row 1: Governance & Existence
      'governance.conceive': { text: 'Policy intent — mandate, charter, guiding principles.', glyph: '●', actors: ['governance-team'], metamodelEntities: ['Strategic Objective'] },
      'governance.design':   { text: 'Controls design — define the guardrails.', glyph: '●', actors: ['compliance-architect'], metamodelEntities: ['Standard'] },
      'governance.build':    { text: 'Compliance build — implement the controls.', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['Standard'] },
      'governance.activate': { text: 'Enforce — turn controls on, audit gating.', glyph: '●', actors: ['audit', 'platform-engineering'], metamodelEntities: ['Platform Service'] },
      'governance.operate':  { text: 'Assurance — continuous monitoring.', glyph: '●', actors: ['audit', 'sre'], metamodelEntities: ['Performance Metric'] },
      'governance.improve':  { text: 'Risk review — periodic re-assessment.', glyph: '●', actors: ['risk-team'], metamodelEntities: ['Performance Metric'] },
      'governance.retire':   { text: 'Policy retire — sunset obsolete mandates.', glyph: '·', actors: ['governance-team'], metamodelEntities: ['Strategic Objective'] },

      // Row 2: Supply & Resources
      'supply.conceive': { text: 'Capacity vision — demand forecast + capacity plan.', glyph: '●', actors: ['capacity-planner'], metamodelEntities: ['Strategic Objective'] },
      'supply.design':   { text: 'Architecture — target-state infrastructure.', glyph: '●', actors: ['enterprise-architect'], metamodelEntities: ['System Function'] },
      'supply.build':    { text: 'Build / procure — provision infrastructure.', glyph: '★', actors: ['platform-engineering'], metamodelEntities: ['Platform Service'] },
      'supply.activate': { text: 'Integration — wire into production.', glyph: '●', actors: ['platform-engineering', 'sre'], metamodelEntities: ['Application Component'] },
      'supply.operate':  { text: 'Monitoring — health, capacity, alerts.', glyph: '●', actors: ['sre'], metamodelEntities: ['Platform Service'] },
      'supply.improve':  { text: 'Utilization — right-sizing, FinOps.', glyph: '●', actors: ['finops', 'sre'], metamodelEntities: ['Performance Metric'] },
      'supply.retire':   { text: 'Retire assets — decommission, dispose.', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['Platform Service'] },

      // Row 3: People & Organization
      'people.conceive': { text: 'Workforce plan — headcount and skills forecast.', glyph: '●', actors: ['workforce-planner'], metamodelEntities: ['Organizational Unit'] },
      'people.design':   { text: 'Org design — team topology, RACI.', glyph: '●', actors: ['org-design'], metamodelEntities: ['Organizational Unit'] },
      'people.build':    { text: 'Hire / train — bring people on.', glyph: '●', actors: ['recruiting', 'l&d'], metamodelEntities: ['Organizational Unit'] },
      'people.activate': { text: 'Mobilize — assign to teams, onboarding.', glyph: '●', actors: ['line-manager'], metamodelEntities: ['Organizational Unit'] },
      'people.operate':  { text: 'Perform & develop — regular work.', glyph: '●', actors: ['line-manager'], metamodelEntities: ['Business Process'] },
      'people.improve':  { text: 'Engagement — pulse surveys, eNPS.', glyph: '●', actors: ['people-ops'], metamodelEntities: ['Performance Metric'] },
      'people.retire':   { text: 'Offboard / reassign — exit or transfer.', glyph: '●', actors: ['people-ops'], metamodelEntities: ['Organizational Unit'] },

      // Row 4: Customer & Demand
      'customer.conceive': { text: 'Need identification — market research, JTBD.', glyph: '●', actors: ['product', 'growth'], metamodelEntities: ['Value Stream'] },
      'customer.design':   { text: 'Journey mapping — personas, friction points.', glyph: '●', actors: ['product-design'], metamodelEntities: ['Journey Touchpoint'] },
      'customer.build':    { text: 'Onboarding — signup flow, verification.', glyph: '●', actors: ['growth', 'engineering'], metamodelEntities: ['Business Process'] },
      'customer.activate': { text: 'Activation — first value moment.', glyph: '★', actors: ['growth'], metamodelEntities: ['Journey Touchpoint'] },
      'customer.operate':  { text: 'Support & service — customer care.', glyph: '●', actors: ['care-ops'], metamodelEntities: ['Business Process'] },
      'customer.improve':  { text: 'Satisfaction & churn — NPS, retention cohorts.', glyph: '●', actors: ['analytics', 'care-ops'], metamodelEntities: ['Performance Metric'] },
      'customer.retire':   { text: 'Offboarding — account closure, GDPR.', glyph: '●', actors: ['care-ops', 'legal'], metamodelEntities: ['Business Object'] },

      // Row 5: Product & Offering
      'product.conceive': { text: 'Market sensing — discovery, opportunity sizing.', glyph: '●', actors: ['product', 'research'], metamodelEntities: ['Business Capability'] },
      'product.design':   { text: 'Catalog & specs — PRD, feature spec.', glyph: '●', actors: ['product-design'], metamodelEntities: ['Business Capability'] },
      'product.build':    { text: 'Configuration — bundle, packaging.', glyph: '●', actors: ['engineering'], metamodelEntities: ['Business Process'] },
      'product.activate': { text: 'Launch — go-to-market, announcement.', glyph: '●', actors: ['product', 'growth'], metamodelEntities: ['Journey Touchpoint'] },
      'product.operate':  { text: 'Catalog management — versioning, lifecycle.', glyph: '●', actors: ['product-ops'], metamodelEntities: ['Business Object'] },
      'product.improve':  { text: 'Performance — adoption, usage, satisfaction.', glyph: '●', actors: ['analytics', 'product'], metamodelEntities: ['Performance Metric'] },
      'product.retire':   { text: 'Sunset — deprecate, migrate users.', glyph: '●', actors: ['product', 'care-ops'], metamodelEntities: ['Business Object'] },

      // Row 6: Operations & Delivery
      'operations.conceive': { text: 'Demand planning — forecast workload.', glyph: '●', actors: ['demand-planner'], metamodelEntities: ['Business Process'] },
      'operations.design':   { text: 'Process design — SOPs, automation.', glyph: '●', actors: ['process-architect'], metamodelEntities: ['Business Process'] },
      'operations.build':    { text: 'Provisioning — environment, tooling.', glyph: '★', actors: ['platform-engineering'], metamodelEntities: ['System Function'] },
      'operations.activate': { text: 'Cut-over — go-live, change window.', glyph: '●', actors: ['change-manager', 'sre'], metamodelEntities: ['System Function'] },
      'operations.operate':  { text: 'Run & maintain — 24/7 operations.', glyph: '★', actors: ['sre', 'noc'], metamodelEntities: ['System Function'] },
      'operations.improve':  { text: 'Quality & incident — post-mortems, SLO.', glyph: '●', actors: ['sre', 'quality'], metamodelEntities: ['Performance Metric'] },
      'operations.retire':   { text: 'Decommission — environment teardown.', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['System Function'] },

      // Row 7: Finance & Value
      'finance.conceive': { text: 'Business case — investment thesis.', glyph: '●', actors: ['finance', 'product'], metamodelEntities: ['Investment Initiative'] },
      'finance.design':   { text: 'Pricing model — tariff, tiers.', glyph: '●', actors: ['pricing-analyst'], metamodelEntities: ['Business Capability'] },
      'finance.build':    { text: 'Funding — budget approval, allocation.', glyph: '●', actors: ['finance', 'cfo'], metamodelEntities: ['Investment Initiative'] },
      'finance.activate': { text: 'Billing activation — start metering.', glyph: '●', actors: ['billing-ops'], metamodelEntities: ['API / Service Contract'] },
      'finance.operate':  { text: 'Revenue & cost — ongoing recognition.', glyph: '★', actors: ['finance', 'revenue-assurance'], metamodelEntities: ['Performance Metric'] },
      'finance.improve':  { text: 'Margin analysis — profitability by segment.', glyph: '●', actors: ['finance', 'analytics'], metamodelEntities: ['Performance Metric'] },
      'finance.retire':   { text: 'Write-off — asset impairment, refunds.', glyph: '●', actors: ['finance'], metamodelEntities: ['Investment Initiative'] },
    };
  }

  function buildTelecomCells() {
    return {
      'governance.conceive': { text: 'Regulatory mandate (e.g. spectrum regulator).', glyph: '●', actors: ['regulatory-affairs'], metamodelEntities: ['Strategic Objective'] },
      'governance.design':   { text: 'Controls design (SOX, ISO27001).', glyph: '●', actors: ['compliance-architect'], metamodelEntities: ['Standard'] },
      'governance.build':    { text: 'Compliance build — DPI, lawful intercept gateway.', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['Standard'] },
      'governance.activate': { text: 'Audit enforce — gating on change windows.', glyph: '●', actors: ['audit'], metamodelEntities: ['Platform Service'] },
      'governance.operate':  { text: 'Lawful intercept — 24/7 compliance.', glyph: '●', actors: ['noc'], metamodelEntities: ['Performance Metric'] },
      'governance.improve':  { text: 'Risk review — quarterly audit cycle.', glyph: '●', actors: ['risk-team'], metamodelEntities: ['Performance Metric'] },
      'governance.retire':   { text: 'Policy repeal — sunset obsolete mandates.', glyph: '·', actors: ['regulatory-affairs'], metamodelEntities: ['Strategic Objective'] },

      'supply.conceive': { text: 'Spectrum vision — RAN roadmap, 5G spectrum planning.', glyph: '●', actors: ['spectrum-planner'], metamodelEntities: ['Strategic Objective'] },
      'supply.design':   { text: 'Core architecture (EPC/5GC).', glyph: '●', actors: ['network-architect'], metamodelEntities: ['System Function'] },
      'supply.build':    { text: 'Equipment install — RAN, core nodes.', glyph: '★', actors: ['field-ops'], metamodelEntities: ['Platform Service'] },
      'supply.activate': { text: 'Network integration — cut-over to live.', glyph: '★', actors: ['noc', 'field-ops'], metamodelEntities: ['Application Component'] },
      'supply.operate':  { text: 'NMS monitoring — alarms, KPIs.', glyph: '●', actors: ['noc'], metamodelEntities: ['Platform Service'] },
      'supply.improve':  { text: 'KPI utilization (erlang).', glyph: '●', actors: ['capacity-planner'], metamodelEntities: ['Performance Metric'] },
      'supply.retire':   { text: 'Equipment retire — 3G sunset.', glyph: '●', actors: ['field-ops'], metamodelEntities: ['Platform Service'] },

      'people.conceive': { text: 'Field force plan — coverage model.', glyph: '●', actors: ['workforce-planner'], metamodelEntities: ['Organizational Unit'] },
      'people.design':   { text: 'NOC/org design — escalation tree.', glyph: '●', actors: ['org-design'], metamodelEntities: ['Organizational Unit'] },
      'people.build':    { text: 'Engineer training — vendor certs.', glyph: '●', actors: ['l&d'], metamodelEntities: ['Organizational Unit'] },
      'people.activate': { text: 'Crew dispatch — first-line ready.', glyph: '●', actors: ['dispatch'], metamodelEntities: ['Organizational Unit'] },
      'people.operate':  { text: 'Performance (OKR).', glyph: '●', actors: ['line-manager'], metamodelEntities: ['Business Process'] },
      'people.improve':  { text: 'Engagement — pulse surveys.', glyph: '●', actors: ['people-ops'], metamodelEntities: ['Performance Metric'] },
      'people.retire':   { text: 'Redeploy — move between regions.', glyph: '●', actors: ['people-ops'], metamodelEntities: ['Organizational Unit'] },

      'customer.conceive': { text: 'Subscriber need — coverage gaps, churn.', glyph: '●', actors: ['product', 'marketing'], metamodelEntities: ['Value Stream'] },
      'customer.design':   { text: 'Tariff plans — pricing, bundles.', glyph: '●', actors: ['product', 'pricing'], metamodelEntities: ['Journey Touchpoint'] },
      'customer.build':    { text: 'SIM provisioning — order capture.', glyph: '●', actors: ['commerce', 'fulfillment'], metamodelEntities: ['Business Process'] },
      'customer.activate': { text: 'Network attach (HLR/HSS) — first call.', glyph: '★', actors: ['noc', 'commerce'], metamodelEntities: ['Journey Touchpoint'] },
      'customer.operate':  { text: 'Customer care (CRM).', glyph: '●', actors: ['care-ops'], metamodelEntities: ['Business Process'] },
      'customer.improve':  { text: 'Churn scoring (ARPU).', glyph: '●', actors: ['analytics'], metamodelEntities: ['Performance Metric'] },
      'customer.retire':   { text: 'Number port (MNP) — out to other carrier.', glyph: '●', actors: ['care-ops'], metamodelEntities: ['Business Object'] },

      'product.conceive': { text: 'Service roadmap (5G, IoT).', glyph: '●', actors: ['product', 'research'], metamodelEntities: ['Business Capability'] },
      'product.design':   { text: 'Service catalog (BSS).', glyph: '●', actors: ['product-design'], metamodelEntities: ['Business Capability'] },
      'product.build':    { text: 'Bundle configuration.', glyph: '●', actors: ['engineering'], metamodelEntities: ['Business Process'] },
      'product.activate': { text: 'Commercial launch.', glyph: '●', actors: ['product', 'marketing'], metamodelEntities: ['Journey Touchpoint'] },
      'product.operate':  { text: 'Catalog lifecycle (OSS).', glyph: '●', actors: ['product-ops'], metamodelEntities: ['Business Object'] },
      'product.improve':  { text: 'Service uptake — adoption tracking.', glyph: '●', actors: ['analytics'], metamodelEntities: ['Performance Metric'] },
      'product.retire':   { text: 'Plan sunset — 2G/3G voice plans.', glyph: '●', actors: ['product', 'care-ops'], metamodelEntities: ['Business Object'] },

      'operations.conceive': { text: 'Traffic forecast — busy hour, region.', glyph: '●', actors: ['demand-planner'], metamodelEntities: ['Business Process'] },
      'operations.design':   { text: 'Network design — capacity, topology.', glyph: '●', actors: ['network-architect'], metamodelEntities: ['Business Process'] },
      'operations.build':    { text: 'Circuit provisioning — EVC setup.', glyph: '★', actors: ['field-ops'], metamodelEntities: ['System Function'] },
      'operations.activate': { text: 'Site cut-over — swap equipment.', glyph: '★', actors: ['noc', 'field-ops'], metamodelEntities: ['System Function'] },
      'operations.operate':  { text: 'NOC operations — 24/7 watch.', glyph: '★', actors: ['noc'], metamodelEntities: ['System Function'] },
      'operations.improve':  { text: 'Fault management — TT, MTTR.', glyph: '●', actors: ['noc', 'quality'], metamodelEntities: ['Performance Metric'] },
      'operations.retire':   { text: 'Site decommission.', glyph: '●', actors: ['field-ops'], metamodelEntities: ['System Function'] },

      'finance.conceive': { text: 'Investment case — CAPEX business case.', glyph: '●', actors: ['finance', 'product'], metamodelEntities: ['Investment Initiative'] },
      'finance.design':   { text: 'Tariff model — regulator-approved.', glyph: '●', actors: ['pricing-analyst'], metamodelEntities: ['Business Capability'] },
      'finance.build':    { text: 'Funding approval.', glyph: '●', actors: ['cfo'], metamodelEntities: ['Investment Initiative'] },
      'finance.activate': { text: 'Billing start — mediation online.', glyph: '●', actors: ['billing-ops'], metamodelEntities: ['API / Service Contract'] },
      'finance.operate':  { text: 'Revenue recognition (ARPU).', glyph: '★', actors: ['revenue-assurance'], metamodelEntities: ['Performance Metric'] },
      'finance.improve':  { text: 'Margin by plan (EBITDA).', glyph: '●', actors: ['finance', 'analytics'], metamodelEntities: ['Performance Metric'] },
      'finance.retire':   { text: 'Asset impairment.', glyph: '●', actors: ['finance'], metamodelEntities: ['Investment Initiative'] },
    };
  }

  function buildDigitalCells() {
    return {
      'governance.conceive': { text: 'Privacy policy — GDPR, CCPA intent.', glyph: '●', actors: ['legal', 'security'], metamodelEntities: ['Strategic Objective'] },
      'governance.design':   { text: 'Controls design (SOC2).', glyph: '●', actors: ['compliance-architect'], metamodelEntities: ['Standard'] },
      'governance.build':    { text: 'Compliance build — guardrails in code.', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['Standard'] },
      'governance.activate': { text: 'Enforce — runtime guardrails.', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['Platform Service'] },
      'governance.operate':  { text: 'Audit log — continuous.', glyph: '●', actors: ['sre', 'security'], metamodelEntities: ['Performance Metric'] },
      'governance.improve':  { text: 'Risk review (pentest).', glyph: '●', actors: ['security-team'], metamodelEntities: ['Performance Metric'] },
      'governance.retire':   { text: 'Policy retire.', glyph: '·', actors: ['legal'], metamodelEntities: ['Strategic Objective'] },

      'supply.conceive': { text: 'Scale vision — capacity for growth.', glyph: '●', actors: ['capacity-planner'], metamodelEntities: ['Strategic Objective'] },
      'supply.design':   { text: 'Cloud architecture (AWS/GCP).', glyph: '●', actors: ['enterprise-architect'], metamodelEntities: ['System Function'] },
      'supply.build':    { text: 'Infra build (Terraform).', glyph: '★', actors: ['platform-engineering'], metamodelEntities: ['Platform Service'] },
      'supply.activate': { text: 'Service mesh.', glyph: '●', actors: ['platform-engineering', 'sre'], metamodelEntities: ['Application Component'] },
      'supply.operate':  { text: 'Observability — metrics, logs, traces.', glyph: '●', actors: ['sre'], metamodelEntities: ['Platform Service'] },
      'supply.improve':  { text: 'Cost/usage (FinOps).', glyph: '★', actors: ['finops', 'sre'], metamodelEntities: ['Performance Metric'] },
      'supply.retire':   { text: 'Infra retire — end-of-service decommission.', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['Platform Service'] },

      'people.conceive': { text: 'Team topology — stream-aligned teams.', glyph: '●', actors: ['workforce-planner'], metamodelEntities: ['Organizational Unit'] },
      'people.design':   { text: 'Org design (pods).', glyph: '●', actors: ['org-design'], metamodelEntities: ['Organizational Unit'] },
      'people.build':    { text: 'Hire / onboard.', glyph: '●', actors: ['recruiting', 'l&d'], metamodelEntities: ['Organizational Unit'] },
      'people.activate': { text: 'Sprint mobilize — first sprint.', glyph: '●', actors: ['line-manager'], metamodelEntities: ['Organizational Unit'] },
      'people.operate':  { text: 'Perf review (360).', glyph: '●', actors: ['line-manager'], metamodelEntities: ['Business Process'] },
      'people.improve':  { text: 'Engagement (eNPS).', glyph: '●', actors: ['people-ops'], metamodelEntities: ['Performance Metric'] },
      'people.retire':   { text: 'Offboard.', glyph: '●', actors: ['people-ops'], metamodelEntities: ['Organizational Unit'] },

      'customer.conceive': { text: 'User need (JTBD).', glyph: '●', actors: ['product', 'research'], metamodelEntities: ['Value Stream'] },
      'customer.design':   { text: 'Persona map.', glyph: '●', actors: ['product-design'], metamodelEntities: ['Journey Touchpoint'] },
      'customer.build':    { text: 'Signup flow.', glyph: '●', actors: ['growth', 'engineering'], metamodelEntities: ['Business Process'] },
      'customer.activate': { text: 'Activation event (aha).', glyph: '★', actors: ['growth', 'product'], metamodelEntities: ['Journey Touchpoint'] },
      'customer.operate':  { text: 'In-product help.', glyph: '●', actors: ['support', 'product'], metamodelEntities: ['Business Process'] },
      'customer.improve':  { text: 'Retention cohort (DAU).', glyph: '●', actors: ['analytics'], metamodelEntities: ['Performance Metric'] },
      'customer.retire':   { text: 'Account deletion (GDPR).', glyph: '●', actors: ['support', 'legal'], metamodelEntities: ['Business Object'] },

      'product.conceive': { text: 'Discovery — opportunity sizing.', glyph: '●', actors: ['product', 'research'], metamodelEntities: ['Business Capability'] },
      'product.design':   { text: 'Feature spec (PRD).', glyph: '●', actors: ['product-design'], metamodelEntities: ['Business Capability'] },
      'product.build':    { text: 'Build sprint.', glyph: '●', actors: ['engineering'], metamodelEntities: ['Business Process'] },
      'product.activate': { text: 'Feature flag launch.', glyph: '★', actors: ['product', 'engineering'], metamodelEntities: ['Journey Touchpoint'] },
      'product.operate':  { text: 'Roadmap management.', glyph: '●', actors: ['product-ops'], metamodelEntities: ['Business Object'] },
      'product.improve':  { text: 'Feature adoption.', glyph: '●', actors: ['analytics', 'product'], metamodelEntities: ['Performance Metric'] },
      'product.retire':   { text: 'Deprecation — sunset, migrate.', glyph: '●', actors: ['product', 'engineering'], metamodelEntities: ['Business Object'] },

      'operations.conceive': { text: 'Demand forecast — capacity, requests.', glyph: '●', actors: ['demand-planner'], metamodelEntities: ['Business Process'] },
      'operations.design':   { text: 'Pipeline design (CI/CD).', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['Business Process'] },
      'operations.build':    { text: 'Provision env (IaC).', glyph: '★', actors: ['platform-engineering'], metamodelEntities: ['System Function'] },
      'operations.activate': { text: 'Deploy to prod (canary).', glyph: '★', actors: ['sre', 'engineering'], metamodelEntities: ['System Function'] },
      'operations.operate':  { text: 'SRE on-call (SLO).', glyph: '★', actors: ['sre'], metamodelEntities: ['System Function'] },
      'operations.improve':  { text: 'Incident review (PSE).', glyph: '●', actors: ['sre', 'quality'], metamodelEntities: ['Performance Metric'] },
      'operations.retire':   { text: 'Env teardown.', glyph: '●', actors: ['platform-engineering'], metamodelEntities: ['System Function'] },

      'finance.conceive': { text: 'Unit economics (LTV).', glyph: '●', actors: ['finance', 'product'], metamodelEntities: ['Investment Initiative'] },
      'finance.design':   { text: 'Pricing tier (SaaS).', glyph: '●', actors: ['pricing-analyst'], metamodelEntities: ['Business Capability'] },
      'finance.build':    { text: 'Funding round.', glyph: '●', actors: ['cfo', 'investors'], metamodelEntities: ['Investment Initiative'] },
      'finance.activate': { text: 'Subscription start (Stripe).', glyph: '●', actors: ['billing-ops'], metamodelEntities: ['API / Service Contract'] },
      'finance.operate':  { text: 'MRR / churn.', glyph: '★', actors: ['revenue-ops', 'finance'], metamodelEntities: ['Performance Metric'] },
      'finance.improve':  { text: 'Cohort margin (CAC).', glyph: '●', actors: ['finance', 'analytics'], metamodelEntities: ['Performance Metric'] },
      'finance.retire':   { text: 'Dunning / refund.', glyph: '●', actors: ['finance', 'support'], metamodelEntities: ['Investment Initiative'] },
    };
  }

})();