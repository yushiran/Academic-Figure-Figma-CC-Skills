# Figure grammar — rules a framework figure must obey

Distilled from paper-framework-figure-studio-pro's prompt contracts (its S1/S4 audit
gates), restated for direct Figma drawing. These are properties of a good paper figure,
independent of how it gets drawn. Apply them at Step-0 planning and again in the
Step-5 screenshot review.

## Evidence rules

1. **Every arrow needs source evidence at both ends.** For each connector you must be
   able to point at the paper text that supports what the upstream produces and what
   the downstream consumes. No decorative arrows.
2. **No false relay.** If A produces `x` and C consumes `x`, and B neither uses,
   transforms, filters, stores nor routes `x`, never draw A→B carrying `x`. Draw A→C,
   or attach `x` to C's input port, or move `x` to the caption.
3. **Source-fidelity table.** Before drawing, classify every visible entity, label,
   symbol and arrow as `direct_source` (paper says it), `strict_logical_inference`
   (safely derivable), or `remove`/`revise`. Anything in the last two classes blocks
   drawing until fixed. This generalises the Step-0 correctness audit.

## Structure rules

4. **Variables live on edges, not in boxes.** Symbols, metrics, weights and other
   quantities go on connectors, ports, forks or small tags — never as boxes that sit
   visually peer-to-peer with modules. (studio-pro calls the violation
   `variable_as_block_error`.)
5. **Operation, not just outcome.** Each core mechanism must show its minimal
   `input → operation → output` chain at the right module. A box showing only the
   result ("difficulty weights") without the operation that produces it ("recall
   profiling → exp(−R) transform") under-draws the method.
6. **Modular, not fragmented.** The figure is a map of modules, not a scatter of
   micro-panels. Inside a module use simple conventional motifs only: process-step
   tokens, decision gates, fork/merge cues, score tags, a light feedback loop. Never a
   second full algorithm inside one box.
7. **One bundled connector between two modules.** Multiple parallel lines between the
   same pair are allowed only when they carry distinct labelled quantities.
8. **Compress repeated entities.** N similar roles/conditions/classes never become N
   full lanes. Use one canonical lane plus compact markers (chips, ×N badges,
   branch-only-where-different). Duplicate lanes are the single fastest way to blow
   the space budget.

## Layout rules

9. **Mainline centred, context subordinate.** The proposed method occupies the central
   visual field; inputs, background and context get a small area budget at the
   periphery. Large empty quadrants and top-heavy context banners are defects, not
   style. (This is the formal version of "把空间充分利用起来".)
10. **Text ownership decided before drawing.** For each fact, decide: in-figure label,
    legend, or caption/body text. In-figure text is for identity and flow; mechanism
    explanations that need full sentences belong in the caption. When a chip needs
    more than ~4 short lines, the surplus moves out.

## Style rules

11. **Restrained publication palette.** One primary accent plus one secondary where
    possible; colour carries meaning (stage identity, flow type) or is absent;
    everything must survive grayscale printing.
12. **Banned AI-render tells:** blue-purple gradients, neon saturation, glossy
    orbs/glass, bokeh, marketing-poster lighting, decorative colour ramps. These make
    a figure read as generated and reviewers notice.

## Screenshot-review error names

Borrowed from studio-pro's issue ledger — useful as a checklist vocabulary when
reviewing your own screenshot: `variable_as_block_error`, `false_relay_data_flow`,
`unbundled_parallel_edges`, `output_substituted_for_operation`,
`fragmented_microblock_scatter`, `excessive_whitespace`, `off_center_mainline`,
`hierarchy_flattening` (everything looks equally important),
`line_semantics_ambiguous` (same line style meaning two things),
`context_inset_dominates_method`.
