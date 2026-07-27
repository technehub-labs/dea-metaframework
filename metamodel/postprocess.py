"""Post-process PlantUML SVG output to support light/dark theme modes.

Strategy:
  1. Remove fixed width/height from root <svg> so it scales
  2. Replace background:#FFFFFF with CSS var reference
  3. Replace text fill #1F2937 / #000000 with currentColor
  4. Replace class border #2C3E50 with CSS var
  5. Inject <style> block in <defs> with light + dark palette + media query
  6. Use cluster data-qualified-name to map layer backgrounds to CSS vars
"""
import re
import sys

src_path = sys.argv[1]
dst_path = sys.argv[2]

content = open(src_path).read()
print(f'Original size: {len(content)}')

# 1. Remove fixed dims from root <svg>
content = re.sub(r'(<svg [^>]*?)\s+width="\d+px"', r'\1', content)
content = re.sub(r'(<svg [^>]*?)\s+height="\d+px"', r'\1', content)
content = re.sub(
    r'(<svg [^>]*?)style="width:\d+px;height:\d+px;background:#FFFFFF;"',
    r'\1style="background:var(--svg-bg, #FFFFFF);"',
    content,
)

# 2. Replace text fills with currentColor
content = content.replace('fill="#1F2937"', 'fill="currentColor"')
content = content.replace('fill="#000000"', 'fill="currentColor"')

# 3. Replace class border with CSS var
content = content.replace('stroke="#2C3E50"', 'stroke="var(--svg-border, #2C3E50)"')

# 3b. Add a per-layer class to each cluster group so CSS can style them precisely.
# PlantUML emits <g class="cluster" data-qualified-name="Layer N. <Name>...">
# We'll inject a `data-layer="N"` attribute on each cluster so we can target it
# directly without fragile substring matching.
LAYER_NAMES_TO_NUMBER = {
    'Ecosystem': 1,
    'Strategic': 2,
    'Business': 3,
    'Digital': 4,
    'Technology': 5,
    'Measurement': 6,
}
def add_data_layer(match):
    full = match.group(0)
    qname = match.group(1)
    for name, num in LAYER_NAMES_TO_NUMBER.items():
        if name in qname:
            return full[:-1] + f' data-layer="{num}">'
    return full

content = re.sub(
    r'<g class="cluster"[^>]*data-qualified-name="([^"]+)"[^>]*>',
    add_data_layer,
    content,
)

# 3c. Remove inline fill on layer cluster paths AND entity box rects so CSS rules win.
# Layer backgrounds use the pastels:
LAYER_PASTELS = {
    '#D6EAF8': '',  # L1 Ecosystem
    '#E8F8F5': '',  # L2 Strategic
    '#FEF9E7': '',  # L3 Business
    '#FDF2E9': '',  # L4 Digital
    '#F4ECF7': '',  # L5 Technology
    '#FADBD8': '',  # L6 Measurement
}
for hex_color in LAYER_PASTELS:
    content = re.sub(
        r'(<g class="cluster"[^>]*>[^<]*<path[^>]*?)fill="' + re.escape(hex_color) + r'"',
        r'\1fill=""',
        content,
    )

# Entity boxes: strip fill="#FFFFFF" so CSS can theme them in dark mode
content = re.sub(
    r'(<g class="entity"[^>]*>.*?<rect\s+)fill="#FFFFFF"',
    r'\1fill=""',
    content,
    flags=re.DOTALL,
)

# 4. Inject <style> block
css_block = '''
<style>
  /* ─── Site integration ─────────────────────────────
     This SVG uses CSS custom properties.
     Default = light theme (PlantUML palette).
     Dark theme auto-applies via prefers-color-scheme.
     Sites that need explicit control add theme-light or
     theme-dark class to <svg> to force a mode. */

  :root, svg {
    --svg-bg: #FFFFFF;
    --svg-text: #1F2937;
    --svg-border: #2C3E50;
    --svg-text-muted: #8B949E;

    --layer-1-bg: #D6EAF8;  /* Ecosystem & Value Network   */
    --layer-2-bg: #E8F8F5;  /* Strategic & Governance      */
    --layer-3-bg: #FEF9E7;  /* Business Operating Model    */
    --layer-4-bg: #FDF2E9;  /* Digital & Intelligence      */
    --layer-5-bg: #F4ECF7;  /* Technology & Execution      */
    --layer-6-bg: #FADBD8;  /* Measurement (Cross-Cutting) */

    color: var(--svg-text);
  }

  @media (prefers-color-scheme: dark) {
    :root, svg {
      --svg-bg: #0f1218;
      --svg-text: #e6edf3;
      --svg-border: #38bdf8;
      --svg-text-muted: #8b949e;

      --layer-1-bg: #0d2630;  /* dark cyan-teal */
      --layer-2-bg: #0d2620;  /* dark emerald   */
      --layer-3-bg: #2e2010;  /* dark amber     */
      --layer-4-bg: #2e1a0d;  /* dark peach     */
      --layer-5-bg: #1f1735;  /* dark violet    */
      --layer-6-bg: #2e1212;  /* dark rose      */
    }
  }

  /* Force light/dark via class for sites that can't rely on media query */
  svg.theme-light {
    --svg-bg: #FFFFFF;
    --svg-text: #1F2937;
    --svg-border: #2C3E50;
    --layer-1-bg: #D6EAF8;
    --layer-2-bg: #E8F8F5;
    --layer-3-bg: #FEF9E7;
    --layer-4-bg: #FDF2E9;
    --layer-5-bg: #F4ECF7;
    --layer-6-bg: #FADBD8;
  }
  svg.theme-dark {
    --svg-bg: #0f1218;
    --svg-text: #e6edf3;
    --svg-border: #38bdf8;
    --layer-1-bg: #0d2630;
    --layer-2-bg: #0d2620;
    --layer-3-bg: #2e2010;
    --layer-4-bg: #2e1a0d;
    --layer-5-bg: #1f1735;
    --layer-6-bg: #2e1212;
  }

  /* Layer cluster backgrounds mapped by data-layer attribute (1-6).
   Use !important because the inline fill="" still has a base value
   in some browsers. */
  g.cluster[data-layer="1"] path { fill: var(--layer-1-bg) !important; }
  g.cluster[data-layer="2"] path { fill: var(--layer-2-bg) !important; }
  g.cluster[data-layer="3"] path { fill: var(--layer-3-bg) !important; }
  g.cluster[data-layer="4"] path { fill: var(--layer-4-bg) !important; }
  g.cluster[data-layer="5"] path { fill: var(--layer-5-bg) !important; }
  g.cluster[data-layer="6"] path { fill: var(--layer-6-bg) !important; }

  /* Entity boxes — use a slightly lighter surface in dark mode */
  g.entity rect:first-of-type {
    fill: var(--entity-bg, #FFFFFF) !important;
  }
  svg.theme-light { --entity-bg: #FFFFFF; }
  svg.theme-dark  { --entity-bg: #1a1d24; }
  @media (prefers-color-scheme: dark) {
    svg:not(.theme-light) { --entity-bg: #1a1d24; }
  }
</style>'''

content = content.replace('<defs/>', '<defs><style type="text/css"><![CDATA[\n' + css_block + '\n]]></style></defs>')

print(f'New size: {len(content)}')

with open(dst_path, 'w') as f:
    f.write(content)
print(f'Saved {dst_path}')