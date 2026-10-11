"""Shared styles embedded in every generated legal-reference guide."""

GUIDE_STYLES = """
* { box-sizing: border-box; }
body {
  margin: 0;
  background: #fff;
  color: #1f2937;
  font-family: system-ui, -apple-system, sans-serif;
  line-height: 1.6;
}
main { max-width: 860px; margin: 0 auto; padding: 2rem 1rem; }
h1, h2, h3 { color: #111827; line-height: 1.3; }
h1 { font-size: clamp(1.75rem, 4vw, 2.25rem); margin: 0 0 1.5rem; }
h2 { font-size: 1.35rem; margin: 2rem 0 0.75rem; }
h3 { font-size: 1.1rem; }
p { margin: 0.75rem 0; }
a { color: #2563eb; text-decoration: none; overflow-wrap: anywhere; }
a:hover { text-decoration: underline; }
a:focus-visible { outline: 2px solid #2563eb; outline-offset: 3px; }
ul { padding-left: 1.5rem; }
li + li { margin-top: 0.5rem; }
.table-scroll { max-width: 100%; overflow-x: auto; }
.table-scroll:focus-visible { outline: 2px solid #2563eb; outline-offset: 3px; }
table { width: 100%; min-width: 640px; border-collapse: collapse; }
caption { text-align: left; font-weight: 600; padding: 0 0 0.75rem; }
th, td { border: 1px solid #e5e7eb; padding: 10px 14px; text-align: left; }
th { background: #f3f4f6; font-weight: 700; }
td { vertical-align: top; }
tbody tr:nth-child(even) { background: #f9fafb; }
.callout {
  margin-top: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  padding: 1rem;
  background: #f8fafc;
}
.callout h2 { margin-top: 0; }
.callout > :last-child { margin-bottom: 0; }
.providers { background: #eff6ff; }
.reference-badge {
  display: inline-block;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 0.125rem 0.5rem;
  background: #f9fafb;
  font-size: 0.875rem;
}
.state-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr));
  gap: 1rem;
  list-style: none;
  padding: 0;
}
.state-grid > li { margin: 0; }
.state-card { border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; }
.state-card h3 { margin: 0; }
.state-card ul { margin-bottom: 0; }
.guide-status { color: #4b5563; font-size: 0.875rem; }
""".strip()
