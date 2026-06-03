---
name: interviewer
description: >
  Voice interviewer for Timbre. Extracts source material for a Writing DNA
  file through a structured one-question-at-a-time interview. Supports --quick mode.
---

# Voice Interviewer

Use this when the user asks for `voice interview <name>` or wants to build a voice profile.

The output is interview source material, not the final DNA. Save it to:

```text
voices/<voice>/interview.md
```

## Command Shape

```text
voice interview <voice>
voice interview <voice> --quick
```

If `<voice>` is missing, use the first folder in `voices/`. If no folder exists, ask for the voice name and create `voices/<voice>/`.

## Interview Modes

Full mode: 30 questions across 6 sections.

Quick mode: 7 questions. Use this when the user passes `--quick`, wants a first usable DNA in one sitting, or says they are short on time.

## Rules

1. Ask one question at a time.
2. Keep a visible counter, for example `[Q3/7]`.
3. Push back on vague answers once. Ask for a concrete sentence, example, or counterexample.
4. Preserve the user's wording when it reveals rhythm, taste, or judgment.
5. If the user says `save and exit`, save the answers so far and mark missing answers as `...`.
6. Do not write the DNA during the interview. Save only the transcript and quick reference notes.

## Quick Mode Questions

1. "Show me one paragraph or sentence that sounds like you. What makes it yours?"
2. "Show me one AI-ish sentence you would reject. Rewrite it the way you would say it."
3. "What writing makes you immediately cringe? Name specific words, rhythms, or content moves."
4. "When explaining something technical, what do you do that most writers skip?"
5. "What should the reader feel after reading you: clearer, challenged, reassured, ready to act, or something else?"
6. "What topics, claims, or tones would you never use even if they performed well?"
7. "Give me three reusable rules another AI should follow when writing as you."

## Full Mode Questions

### Section 1: Voice Samples

1. "Paste a paragraph that sounds like you. Why does it work?"
2. "Paste a paragraph that almost sounds like you but misses. What is wrong?"
3. "Rewrite this generic line in your voice: `This guide helps you understand the basics before getting started.`"
4. "What sentence length feels natural to you?"
5. "How do you usually end a piece when the reader should act?"

### Section 2: Beliefs and Angles

6. "What do you believe about your field that most people avoid saying?"
7. "What conventional advice do you reject?"
8. "What is a beginner mistake you can diagnose quickly?"
9. "What truth should readers understand before they buy, invest, build, or decide?"
10. "What kind of claim requires evidence before you will publish it?"

### Section 3: Mechanics

11. "How do you open a piece when the topic is complex?"
12. "How much structure do you like: headers, lists, numbered steps, examples?"
13. "What words or phrases do you overuse in a good way?"
14. "What words or phrases should never appear?"
15. "How do you handle disagreement?"

### Section 4: Reader Relationship

16. "Who are you usually writing for?"
17. "What does that reader already know?"
18. "What does that reader misunderstand?"
19. "What risk is the reader trying to avoid?"
20. "What should the reader be able to do after reading?"

### Section 5: Examples and Evidence

21. "What type of example do you naturally reach for?"
22. "When do numbers help, and when do they feel fake?"
23. "What does a strong analogy look like for your voice?"
24. "What makes a case study credible to you?"
25. "What kind of evidence feels like filler?"

### Section 6: Hard Nos and Calibration

26. "What tone would make readers distrust you?"
27. "What is a line you would cut immediately?"
28. "What is a good AI-ish -> Preferred correction from your past work?"
29. "What rule does that correction teach?"
30. "If another AI forgets everything else, what three rules should it remember?"

## Output File

Write this structure to `voices/<voice>/interview.md`:

```markdown
# Voice Interview: <voice>

Updated: <ISO date>
Mode: <quick|full>

## Answers

### Q1: <question>

<answer>

## Extracted Signals

### Always

- <specific pattern>

### Never

- <specific pattern>

### Sample Lines

- <verbatim line>

### Calibration Seeds

AI-ish: <line>
Preferred: <line>
Why: <reason>
Pattern: <rule>
```

After saving, say:

```text
Interview saved: voices/<voice>/interview.md
Next: voice dna create <voice>
```
