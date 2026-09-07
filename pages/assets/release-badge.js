/**
 * Release badge — surfaces the latest release tag + name for the
 * current repository from the GitHub Releases API.
 *
 * Usage (on the ECF matrix page):
 *
 *   <div id="mf-release-badge" data-repo="dea-metaframework"></div>
 *
 * The module fetches
 *   https://api.github.com/repos/technehub-labs/{repo}/releases/latest
 * once per page load (cached 1h in localStorage), then writes a small badge
 * into the host element:
 *
 *   Latest release · v2.3.0 — ECF Domain Restructure · 2026-09-07
 *
 * Graceful fallback:
 *   - On any fetch / JSON failure → element stays empty, no console error
 *   - On HTTP 403 (rate limit) → cached value if present, else empty
 *   - On HTTP 404 (no releases) → element shows "No releases published yet"
 */

(function () {
  'use strict';

  const ORG = 'technehub-labs';
  const CACHE_KEY_PREFIX = 'th_release_';
  const CACHE_TTL_MS = 60 * 60 * 1000; // 1 hour

  /**
   * Render the badge into a host node. Returns true on render, false if empty.
   */
  async function mount(host) {
    if (!host) return false;
    const repo = host.dataset.repo;
    if (!repo) return false;

    let release = null;
    try {
      release = await loadLatestRelease(repo);
    } catch (_e) {
      // loadLatestRelease handles its own errors; this catch is defensive.
    }

    if (!release) {
      host.innerHTML = '<span class="mf-release-empty">No release published yet.</span>';
      return false;
    }

    const tag = release.tag_name || '';
    const name = release.name || tag;
    const date = formatDate(release.published_at);
    const url = release.html_url || `https://github.com/${ORG}/${repo}/releases`;

    host.innerHTML = `
      <a class="mf-release-badge" href="${escapeAttr(url)}" target="_blank" rel="noopener" aria-label="Latest release ${escapeAttr(tag)} — ${escapeAttr(name)}">
        <span class="mf-release-dot" aria-hidden="true"></span>
        <span class="mf-release-label">Latest release</span>
        <span class="mf-release-tag">${escapeHtml(tag)}</span>
        <span class="mf-release-name">— ${escapeHtml(name)}</span>
        ${date ? `<span class="mf-release-date">· ${escapeHtml(date)}</span>` : ''}
        <span class="mf-release-arrow" aria-hidden="true">↗</span>
      </a>
    `;
    return true;
  }

  /**
   * Load the latest release for a repo, with localStorage cache.
   * Returns null on any failure.
   */
  async function loadLatestRelease(repo) {
    const cacheKey = CACHE_KEY_PREFIX + repo;
    const cached = readCache(cacheKey);
    if (cached) return cached;

    const url = `https://api.github.com/repos/${ORG}/${repo}/releases/latest`;
    const resp = await fetch(url, {
      headers: { Accept: 'application/vnd.github+json' },
    });

    if (resp.status === 404) {
      // Repo exists but has no releases yet — cache the null result to avoid
      // hammering the API on every page load.
      writeCache(cacheKey, null);
      return null;
    }

    if (!resp.ok) {
      // 403 (rate limit) or other transient failure — do NOT cache, allow
      // retry on next page load.
      console.warn(`[release-badge] ${url} ${resp.status}`);
      return null;
    }

    const release = await resp.json();
    writeCache(cacheKey, release);
    return release;
  }

  function readCache(key) {
    try {
      const raw = window.localStorage.getItem(key);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || !parsed.value) return parsed.value === null ? null : null;
      if (Date.now() - parsed.at > CACHE_TTL_MS) return null;
      return parsed.value;
    } catch (_e) {
      return null;
    }
  }

  function writeCache(key, value) {
    try {
      window.localStorage.setItem(key, JSON.stringify({ at: Date.now(), value }));
    } catch (_e) {
      // localStorage may be disabled / quota exceeded — silently skip.
    }
  }

  function formatDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }
  function escapeAttr(s) {
    return escapeHtml(s).replace(/'/g, '&#39;');
  }

  // Auto-mount any [data-release-repo] host nodes on DOMContentLoaded.
  function autoMount() {
    const hosts = document.querySelectorAll('[data-release-repo]');
    hosts.forEach((h) => mount(h));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoMount);
  } else {
    autoMount();
  }

  // Public API for other scripts that want to mount a badge imperatively.
  window.__TNH_RELEASE_BADGE__ = { mount, loadLatestRelease };
})();