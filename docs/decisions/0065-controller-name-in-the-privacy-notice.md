# 0065: The controller's name in the Privacy notice

**ID:** SE-11  
**Status:** Accepted (founder, 21 Nov 2026, prompt windows)  
**Date:** 2026-11-21  
**Stage:** 5b  
**Amends (no older text is rewritten):** `AGENTS.md` rule 5 (one clause: the controller's name may be written in the Privacy notice); [0063](0063-pilot-privacy-and-anonymous-chat-first.md) point 6 (where the founder's name appears was "Ask me again later").  
**Design:** [`2026-11-21-anonymous-chat-design.md`](../superpowers/specs/2026-11-21-anonymous-chat-design.md), section 5.

## Context
0063 made the founder the controller, as a private individual, with a privacy@ contact, and left open where the founder's name appears. UK GDPR Article 13(1)(a) says the notice must give "the identity and the contact details of the controller" ([legislation.gov.uk](https://www.legislation.gov.uk/eur/2016/679/article/13), read 21 Nov 2026), so an email address alone is not enough. The repository is public (rule 5: no real personal data), so writing a name into the notice needs an exception to rule 5, and rule 5 is an integrity rule: it changes only through a recorded decision.

## Options
1. **"Filled in at deploy"** (the agent's recommendation): the name is a setting on the server, never in the repository. The history stays free of the name. The cost is a notice in the repository that shows a placeholder, so the text a visitor reads is not the text reviewed.
2. **"Exception to rule 5"** (chosen): the name is written into the notice in the repository. The notice reviewed is the notice shown. The cost is that the name is in the public history for good.
3. **"Ask me again later"**: no change now. The chat cannot go public until the notice names the controller, so this only delays the choice.

## Decision
The founder's answers, 21 Nov 2026, in prompt windows:
- **"Exception to rule 5"**, over "Filled in at deploy" and "Ask me again later".
- **Name:** the founder's full name as on their commits ("(Recommended)"): **Sunkanmi Olawuwo**.
- **Contact:** **privacy@vestagraph.co.uk** ("privacy@vestagraph.co.uk (Recommended)"; IN-06 registered both domains).

Rule 5 gains one clause: "except the controller's name in the Privacy notice (decision 0065)".

## Consequences
- **The name stays in the public history for good**, even if later removed from the files.
- **Only these files may carry the name:** this record, the PRIV scenario or scenarios that name the controller in `docs/specs/pilot/public-pages.feature`, and the Privacy notice board on the design canvas, plus the built Privacy notice page when it is made. It is not written in `AGENTS.md`, the register, the status file, commit messages or pull requests.
- **Revisit if the controller changes**, for example if a company takes over, the project starts trading (0063 point 7) or the founder asks for the name to be removed.
