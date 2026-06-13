---
name: eng-front-end-design
description: "Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics while maintaining usability."
---

# Front-End Design

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details, usability, and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints. They may also specify a style or provide a markdown of a design system they already have.

## Design Thinking

Before coding, understand the context and commit to the user's aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: If the user specifies an aesthetic direction, commit fully to it. If not, choose a direction that fits the product context: minimal, modern, playful, editorial, or industrial.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this memorable? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. The key is intentionality, not intensity.

**Prototype Priority**: At prototype stage, optimize for **clarity and usability** over visual experimentation. Ensure:
- Readable typography and sufficient contrast
- Clear visual hierarchy and navigation
- Accessible focus states and keyboard navigation
- Fast load times (prioritize performance over elaborate effects)

**Generate a pilot image** before writing code. Use the workspace script:
```bash
python3 /Users/thagstn/Documents/ai-tools/scripts/generate-image.py "<detailed visual description of the design>" <project-path>/research/pilot.png
```
Show the generated image to the user and get approval before proceeding to implementation.

Implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Accessible and usable across devices
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Ground all choices in the aesthetic direction. If the user has not specified one, apply the direction chosen in Design Thinking. Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and readable. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics — unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations sparingly for high-impact moments. Prioritize CSS-only solutions. One well-orchestrated page transition creates more delight than scattered micro-interactions.
- **Spatial Composition**: Intentional layouts with consistent spacing. Generous negative space OR controlled density — chosen deliberately.
- **Backgrounds & Visual Details**: Create atmosphere without overloading. Use contextual effects that match the overall aesthetic.
- **Icons & Imagery**: Use real SVG icons such as Lucide, Heroicons, or Phosphor instead of emoji. Use real imagery, product screenshots, or purposeful decorative graphics instead of blank placeholders.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts) unless explicitly requested. AVOID cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts, and cookie-cutter design.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision and feature maturity. MVP pages should be clean, fast, and accessible. Elaborate animations are for polished features, not prototype scaffolding.

Remember: The agent is capable of extraordinary creative work. Don't hold back — show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
