---
name: image-prompt
description: >
  Generate optimized prompts for Google's Nano Banana image generators (Nano Banana 2
  and Nano Banana Pro). Use when the user invokes /image-prompt or asks to create, write,
  craft, or generate a prompt for Nano Banana, Gemini image generation, or AI image
  creation. Also triggers when the user says "image prompt", "nano banana prompt",
  "nano banana 2", or "help me describe an image".
---

<!--
  Nano Banana Prompt Generator — Agent Skill
  ===========================================

  An agent skill that helps you craft optimized prompts for Google's
  Nano Banana image generators (Nano Banana 2 and Nano Banana Pro).

  Compatible with Claude Code, Gemini CLI, and other tools that support
  the agent skill format (SKILL.md with YAML frontmatter).

  ## Installation

  IMPORTANT: The YAML frontmatter (the --- block) MUST be the very first
  thing in this file. Do not place comments or content before it.

  For Claude Code:
     mkdir -p ~/.claude/skills/image-prompt
     # Copy this file to ~/.claude/skills/image-prompt/SKILL.md

  For Gemini CLI (and cross-platform):
     mkdir -p ~/.agents/skills/image-prompt
     # Copy this file to ~/.agents/skills/image-prompt/SKILL.md

  Restart your tool or start a new session. The skill will be available
  as /image-prompt.

  ## What This Skill Does

  - Asks you targeted questions about your image idea (subject, mood,
    lighting, style, composition, etc.)
  - Generates an optimized natural-language prompt following Google's
    official guidance
  - Explains why each element was chosen
  - Supports iterative refinement until you're happy with the prompt
  - The generated prompt can be copied into the Gemini web app, Google
    AI Studio, or any tool that supports Nano Banana image generation
  - For direct CLI image generation, see the "nanobanana" Gemini CLI
    extension: https://github.com/gemini-cli-extensions/nanobanana

  ## Sources

  Prompting advice is based on:
  - Google Blog: "7 tips to get the most out of Nano Banana Pro"
    https://blog.google/products/gemini/prompting-tips-nano-banana-pro/
  - Google Blog: "Nano Banana 2: Combining Pro capabilities with lightning-fast speed"
    https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/
  - Google AI for Developers: Nano Banana image generation docs
    https://ai.google.dev/gemini-api/docs/image-generation

  ## Note

  Model availability, plan tiers, and capability limits (e.g., number of
  reference images, resolution ranges) may change as Google updates its
  products. The prompting principles — natural language, specificity,
  creative direction over keyword lists — are stable best practices.

  Author: Kenneth Kousen
  Last updated: 2026-02-28
-->

# Nano Banana Prompt Generator

Generate high-quality, optimized prompts for Google's Nano Banana image generators,
based on Google's official prompting guidance.

## Choosing a Model

Both models use the same prompting approach. Help the user pick the right one if they're unsure:

| | **Nano Banana 2** | **Nano Banana Pro** |
|---|---|---|
| **Speed** | Fast (Flash-based) | Slower, highest fidelity |
| **Best for** | Rapid iteration, everyday use | Maximum detail and factual accuracy |
| **Default in** | Gemini app, Google Search | Premium plans (AI Pro/Ultra) |
| **Resolution** | 512px to 4K (specify explicitly) | Up to high-res |
| **Characters** | Up to 5 consistent characters | Via reference images |
| **Objects** | Up to 14 consistent objects | Up to 14 reference images |
| **Instruction following** | Enhanced — handles complex prompts well | Strong |

Nano Banana 2 is the default for most users. Recommend Pro only when the user needs
maximum fidelity or highly accurate real-world detail.

> **Note:** Model availability and plan details may change. Check Google's current
> documentation if the above table seems outdated.

## Core Principles

Both models understand intent, physics, and composition.
They reward **clear creative direction** over keyword lists.

### Golden Rules

1. **Natural language over tag soup** — Write as if briefing a human artist, not listing keywords.
   - BAD: "dog, park, sunset, 4k, realistic, cinematic"
   - GOOD: "A golden retriever bounding through a sun-dappled park at golden hour, shot from a low angle with shallow depth of field"

2. **Specificity matters** — Define subjects precisely with materiality, texture, and detail.
   - Instead of "a woman": "a sophisticated elderly woman wearing a vintage Chanel-style tweed suit"
   - Include materials: "matte finish," "brushed steel," "soft velvet," "weathered leather"

3. **Provide context about purpose** — Mention the use case or audience.
   - "Create a hero image for a premium coffee brand's website" helps the model infer professional lighting, composition, and mood.

4. **Edit, don't re-roll** — When a generated image is mostly correct, request specific conversational changes rather than starting over.

## Workflow

### Step 1: Gather the User's Vision

Ask the user to describe what they want. If their description is vague, ask targeted questions to fill in these dimensions:

| Dimension | What to ask | Examples |
|-----------|------------|---------|
| **Subject** | Who or what is the main focus? | Person, object, scene, abstract concept |
| **Setting/Environment** | Where does this take place? | Urban, nature, studio, fantastical |
| **Mood/Atmosphere** | What feeling should it evoke? | Serene, dramatic, playful, mysterious |
| **Style** | What visual style? | Photorealistic, watercolor, cinematic, editorial, retro, anime |
| **Composition** | How should it be framed? | Close-up, wide shot, bird's eye, rule of thirds |
| **Lighting** | What lighting conditions? | Golden hour, dramatic side-light, soft diffused, neon |
| **Purpose/Use case** | Where will this image be used? | Social media, website hero, print poster, presentation |
| **Text (if any)** | Any text to render in the image? | Put exact text in quotation marks |
| **Resolution** | What resolution/aspect ratio? | 512px, 1080p, 4K; 16:9, 9:16, 1:1 |

**Do not ask all questions at once.** Start with the most important gaps based on what the user already provided. Ask 2-3 questions maximum per round.

### Step 2: Build the Prompt

Construct the prompt using this structure (not all elements are required — use what's relevant):

```
[Style/medium] of [specific subject with details] in [setting/environment],
[action or pose], [lighting description], [mood/atmosphere],
[camera angle/composition], [additional details: texture, color palette, materiality].
[Purpose context if relevant.]
```

**Key techniques to apply:**

- **Camera language**: Use cinematic terms — "wide establishing shot," "tight close-up," "over-the-shoulder," "Dutch angle," "shallow depth of field"
- **Lighting specifics**: "Rembrandt lighting," "backlit with rim light," "soft window light from the left," "dramatic chiaroscuro"
- **Material and texture**: "brushed aluminum," "hand-knit wool," "cracked leather," "translucent glass"
- **Color direction**: "muted earth tones," "high-contrast complementary colors," "monochromatic blue palette"
- **Text rendering**: Place exact text in quotation marks — Nano Banana has state-of-the-art text legibility
- **Resolution**: For Nano Banana 2, explicitly request resolution (512px up to 4K) when it matters
- **Aspect ratio**: Suggest appropriate ratio for the use case (16:9 landscape, 9:16 portrait, 1:1 square)

### Step 3: Present the Prompt with Rationale

Output the prompt in a clearly marked block, followed by brief rationale notes explaining key choices:

```
PROMPT:
─────────────────────────────────────────────
[The generated prompt text]
─────────────────────────────────────────────

WHY THESE CHOICES:
- [Element]: [Brief explanation of why this detail was included]
- [Element]: [How it helps the model produce better results]
```

### Step 4: Offer Refinement

After presenting the prompt, ask the user:

> "Would you like to adjust anything? I can refine the style, composition, lighting, mood, or any other element. You can also ask me to create a variant with a different approach."

Continue iterating until the user is satisfied.

## Special Capabilities to Leverage

Mention these to the user when relevant:

### Reference Images and Consistency
Both models support multi-image context for consistency:
- **Nano Banana 2**: Up to 5 consistent characters and 14 consistent objects per workflow
- **Nano Banana Pro**: Up to 14 reference images (6 with high fidelity)

Instruct the model with:
- "Use the uploaded images as a strict style reference"
- "Keep the character from Image 1 but place them in the setting from Image 2"
- For character consistency: "Keep facial features exactly the same as the reference"
- For storyboarding: "The identity and attire of all characters must stay consistent throughout"

### Conversational Editing
After generating an image, the user can type natural-language edits:
- "Change the sunny day to a rainy night"
- "Remove the person in the background and add a potted plant"
- "Make the text neon blue instead of white"
The model adjusts lighting, reflections, and physics automatically.

### Text in Images
Both models have state-of-the-art text rendering and support translation/localization of text
within images. Always put exact text in quotation marks in the prompt. Specify text style
if needed: "bold sans-serif," "handwritten script," "retro neon sign." For localization,
try: "Translate the text in this image to Japanese."

### Dimensional Translation
The model can convert between 2D and 3D:
- Hand-drawn sketches to photorealistic renders
- Floor plans to 3D room visualizations
- Wireframes to high-fidelity UI mockups

### Structural Control
Users can upload layout sketches to control composition:
- Hand-drawn sketches defining where text and objects should go
- Grid layouts for tile-based designs
- Wireframes for UI mockup generation

## Anti-Patterns to Avoid

When reviewing or building prompts, watch for and fix these:

- **Tag soup**: Disconnected keyword lists — rewrite as natural sentences
- **Vague subjects**: "a person" or "a building" — add specific details
- **Missing mood/lighting**: These dramatically affect output quality — always include them
- **No context**: Omitting the purpose/use case — include it when relevant
- **Over-prompting**: Contradictory or excessive details that confuse the model — keep it coherent and focused

## Example Prompts

Use these as calibration for quality:

**Product photography:**
> A flat lay of artisanal coffee beans spilling from a matte black ceramic cup onto a weathered oak table, soft directional window light from the upper left, warm earth tones with deep shadows, shot from directly above, styled for a premium coffee brand's Instagram feed.

**Portrait:**
> A cinematic medium close-up portrait of a jazz musician mid-performance, eyes closed, sweat glistening under warm amber stage lighting, shallow depth of field with bokeh from string lights in the background, shot on what looks like 35mm film with natural grain.

**Text-heavy design:**
> A vintage-style concert poster with the text "MIDNIGHT REVERIE" in bold art deco typography at the top, a silhouette of a saxophone player against a deep indigo night sky with a full moon, "Live at The Blue Note — March 15, 2026" in smaller elegant serif type at the bottom, gold and navy color palette.

**Fantasy/Illustration:**
> A lush watercolor illustration of a hidden forest library, towering bookshelves made from living trees with glowing mushrooms as reading lamps, a cozy armchair draped in moss-green velvet, shafts of golden sunlight filtering through the canopy above, whimsical and enchanting atmosphere.

## Sources

Prompting advice in this skill is based on:

- [7 tips to get the most out of Nano Banana Pro](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/) — Google Blog
- [Nano Banana 2: Combining Pro capabilities with lightning-fast speed](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/) — Google Blog
- [Nano Banana image generation](https://ai.google.dev/gemini-api/docs/image-generation) — Google AI for Developers
