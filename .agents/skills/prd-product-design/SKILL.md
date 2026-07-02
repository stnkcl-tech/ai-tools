---
name: prd-product-design
description: "Produce intuitive, easy-to-use product designs grounded in Don't Make Me Think principles. Use when designing UI/UX, creating or refining a design system, generating wireframes, mockups, or frontend concepts for a project."
---

# Product Design

Design usable, intuitive interfaces by first understanding the project and its existing design system, then applying principles from *Don't Make Me Think*.

## Rules

1. **Never assume.** If information is missing, ask before designing.
2. **Present a proposal before executing.** Show the plan or direction and get approval before building assets, code, or a design system.
3. **Show visual comparisons instead of text descriptions whenever possible.** Use wireframes, mockups, or generated pilot images rather than long paragraphs.

## Step 1: Confirm Project Direction

Before producing any design, read the project context:

- `AGENTS.md`
- `README.md`
- Any PRD, product brief, or vision document
- Existing user stories, job stories, or research notes

Look for answers to:
- What problem does this product solve?
- Who is the target user?
- What is the core value proposition?
- What phase is the project in (discovery, delivery, growth)?

If any of these are missing or unclear, stop and ask the user:
- "What is this project?"
- "Who is it for?"
- "What problem does it solve for them?"
- "What should a user be able to do after interacting with this design?"

## Step 2: Check for an Existing Design System

Look for any of the following in the repo:

- Design tokens (CSS variables, JSON/YAML tokens)
- Style guide or component library documentation
- Theme files (Tailwind config, CSS framework, SCSS variables)
- Figma links or exported design files
- Existing components, icons, or color/type scales
- Accessibility guidelines (WCAG targets, focus styles)

If a design system exists, use it as the foundation. Do not invent new colors, type, spacing, or components unless the existing system is incomplete or the user asks for a change.

If no design system exists, move to Step 4.

## Step 3: Design with Don't Make Me Think Principles

Read `references/dont-make-me-think.md` before producing designs.

Apply the principles as a checklist for every screen or component:

- Make the purpose self-evident at a glance.
- Follow conventions unless a better pattern is justified.
- Establish a clear visual hierarchy with one primary action.
- Group related content into clearly defined areas.
- Make clickable elements obviously clickable.
- Reduce noise and decorative clutter.
- Format content for scanning: headings, bullets, short paragraphs.
- Cut copy aggressively.
- Break complex tasks into unambiguous clicks.
- Pass the trunk test: site ID, page name, main sections, local options, search.
- Design for forgiveness and error recovery.
- Design mobile as a simplified experience, not a shrunken desktop.

## Step 4: Build a Design System When None Exists

If no design system is found, do not invent one silently. Present a proposal first, then ask clarifying questions such as:

- What brand personality should the product convey? (e.g., playful, serious, premium, friendly)
- Are there existing brand colors, logos, or fonts?
- Light mode, dark mode, or both?
- What devices and screen sizes matter most?
- Are there accessibility requirements? (e.g., WCAG AA compliance)
- Any competitors or references the user likes or dislikes?

Then create a minimal starter system:

- Color palette (primary, secondary, neutrals, semantic colors)
- Typography scale (font family, sizes, weights, line heights)
- Spacing scale
- Border radius and shadow styles
- Button and input styles
- Icon library choice
- Layout grid and breakpoints

Store the design system in a `design-system.md` file at the project root or in a `docs/` or `research/` folder, depending on the project structure.

## Step 5: Produce Visual Output

Always prefer visual artifacts over text descriptions.

Options for visual output:

- **Wireframes**: Low-fidelity structure using ASCII, Excalidraw, Mermaid, or simple HTML/CSS.
- **Mockups**: Higher-fidelity static images or HTML prototypes.
- **Pilot images**: Generate a visual concept with the workspace script:
  ```bash
  python3 /Users/thagstn/Documents/ai-tools/scripts/generate-image.py "<detailed visual description>" <project-path>/research/design-concept.png
  ```
  Show the generated image and get approval before moving to implementation.

When presenting multiple options, show them side by side and explain the trade-offs in one or two sentences each.

## Step 6: Hand Off to Implementation

Once the design direction is approved, convert it into implementation-ready output:

- Annotated wireframes or mockups
- Component list with props and states
- Copy and content specifications
- User flows or interaction notes
- Accessibility considerations

If building frontend code, invoke the `eng-front-end-design` skill for high-quality implementation.

## Output Checklist

Before finishing, confirm:
- [ ] Project direction and target user are documented or confirmed by the user.
- [ ] Existing design system was checked and used or a new one was proposed and approved.
- [ ] Don't Make Me Think principles were applied.
- [ ] Visual artifacts were produced and reviewed.
- [ ] The user approved the direction before any final code or assets were built.
