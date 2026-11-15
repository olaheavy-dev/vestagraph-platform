> Research for the "Use in ChatGPT or Claude" page (decision 0056), done at the founder's request ("Research them first", 15 Nov 2026).

# Research note: using the pilot's MCP server from ChatGPT and Claude

Read on 15 Nov 2026, official sources only. Searches used generic terms only. Quotes are short and, where a fetch tool summarised a page, marked "(summarised by the fetch tool)".

**Headline finding:** OpenAI has changed its docs. The page our records cite (`developers.openai.com/api/docs/guides/developer-mode`) is now titled "Add custom MCP server" and says to use **ChatGPT Plugins**, not Developer mode. The text of that page no longer mentions developer mode. The Settings, Connectors, Advanced path in our records is therefore out of date for OpenAI's current docs. The help centre pages (help.openai.com) returned HTTP 403 to my fetch tool, so I could only see them through search snippets.

## 1. ChatGPT "developer mode": what it is, how to turn it on, plans
- Current OpenAI developer docs no longer describe developer mode. The only trace is a hidden page anchor named `what-is-chatgpt-developer-mode`. The page now says: "Connect your Model Context Protocol (MCP) server to ChatGPT as a plugin."
- Older help-centre wording (search snippet, not read in full): developer mode, apps and full MCP support "available to ChatGPT Business and Enterprise/Edu customers on the web"; admin turns it on first. Its article title has changed three times (developer mode and MCP connectors; developer mode and full MCP apps; connecting custom MCP servers in ChatGPT).
- Current help-centre wording (search snippet, 12584461-connecting-custom-mcp-servers-in-chatgpt, updated about 16 Oct 2026, from the search snippet's "about 30 days before today" on 15 Nov 2026): Business, only admins and owners can create and publish; Enterprise/Edu, admins can give selected members creation rights through role-based access control (RBAC), publishing stays with admins; the admin permission is called "Create plugins with MCPs" and is "Off by default in Enterprise workspaces".
- Free, Plus and Pro: not stated in the official pages I could read.
- Not stated in official docs: any "turn on developer mode" step under the current wording.

## 2. Trade-offs and warnings, as OpenAI states them
- "Only connect to MCP servers you trust. An untrusted server may access or steal information shared through app use, or trick ChatGPT into using tools in unintended ways."
- Write actions need confirmation by default; wrong writes can destroy, alter or share data. Tools without the `readOnlyHint` annotation are treated as write actions. Remembering an approval for a conversation means later write actions in it may run without asking.
- ChatGPT supports "both read and write tools".
- Workspace permissions and security restrictions, including Lockdown, apply.
- Memory off or other developer-mode-specific warnings: not stated in the pages I could read.

## 3. Adding a server by URL in ChatGPT
Steps (developers.openai.com custom-mcp-server page):
1. Go to ChatGPT Plugins (chatgpt.com/plugins).
2. Select the plus button, then "Add custom MCP server".
3. Enter a name and an optional description.
4. Under Connection, enter the Server URL (public HTTPS, or a Secure MCP Tunnel for private servers).
5. Configure authentication.
6. Review the risk warning and select "I understand and want to continue."
7. Select "Create as a plugin."
8. Install it, then "Start a new conversation with the plugin enabled."
- Transports: SSE and streaming HTTP.
- Authentication: "Authentication options include OAuth, No authentication, and OAuth or no authentication." So "No authentication" exists. Mixed mode: initialize and list-tools use no auth, and each tool uses OAuth or none per its security scheme.
- Admin: see section 1 (Business admins or owners; Enterprise/Edu RBAC and the "Create plugins with MCPs" permission). The plugin appears "in your personal plugins or the workspace where you created it". Whether other ordinary users can then use a server one person added: not stated in official docs.

## 4. ChatGPT interactive widgets
- Official: "Components run inside an iframe in ChatGPT" and use the MCP Apps bridge. Declare the UI with `_meta.ui.resourceUri` and MIME type `text/html;profile=mcp-app`; `_meta["openai/outputTemplate"]` is accepted as an alias. "Keep tools useful without UI so clients that don't render components can still finish the workflow."
- "If the server returns optional UI, test both the component and the model-readable result." (connect-and-test page).
- The plugin review process "checks the declared policy against the UI behavior." Owners (or members with Apps Management Write) submit; "Once approved, you choose when to publish."
- Whether a public, unlisted, unsubmitted server's widget shows for an ordinary user: **not stated** in official docs. Pages are silent on plans and on conditions for rendering.
- OpenAI's own community forum (not an official-source domain, so not relied on) has anecdotes of widgets failing on some accounts and working on others.

## 5. Claude: custom connector by URL
Source: claude.com/docs/connectors/custom/remote-mcp and support.claude.com article 11175166.
- Plans: "Free, Pro, Max, Ultra, Team, and Enterprise". Free is limited to one custom connector.
- Free, Pro, Max, Ultra: Customize > Connectors, Add, Add custom connector, enter name and server URL, Continue, choose authentication (keep options marked Detected), Add, then Connect if shown.
- Team and Enterprise: an Owner (or on Enterprise a member with a custom role that can manage libraries) goes to Organization settings > Connectors, Add, Custom, Web, enters name and URL, chooses authentication, Add. Members then click Connect under Customize > Connectors. Members without a role "can't add a custom connector yourself".
- Authless supported: "**No sign-in**: anyone with access to the server URL can use the connector." (the older help text says "No sign in").
- URL example in the docs: `https://mcp.example.com/mcp`; a URL ending `/sse` selects the older SSE transport.
- Warning: "Custom connectors allow connections to unverified services. Claude can access and perform actions within these services." Advice: only connect to trusted servers, watch for prompt injection, review tool approvals, be careful with "Always allow".
- Connections come from Anthropic's cloud, so the server must be publicly reachable over HTTPS on port 443.

## 6. Claude interactive UI
- Anthropic (blog, 26 Jan 2026): interactive connectors "Available in Claude on mobile, web and desktop for Free, Pro, Max, Ultra, Team, and Enterprise plans." MCP Apps lets "any MCP server deliver interactive connectors with a rich user interface."
- Anthropic (blog, 10 Nov 2026): fuller in-chat apps roll out on web and desktop "once your account is updated to the new Claude experience or your organization turns it on"; available "where a connector supports it".
- Support article 11175166: "Some connectors can open interactive interfaces in the chat"; Team and Enterprise owners can disable specific tool calls that render interfaces.
- MCP site (modelcontextprotocol.io/extensions/apps/overview): MCP Apps "currently supported by Claude, Claude Desktop, VS Code GitHub Copilot, Microsoft 365 Copilot, Goose, Postman, MCPJam, and Archestra.AI". ChatGPT is not on that list.
- Whether a custom connector added by URL (not in the directory) renders UI: **not stated** (the January blog implies yes; neither page says so for custom connectors).

## 7. What the host sends when a tool is called
- ChatGPT (developers.openai.com/plugins/reference), `_meta` fields: `openai/locale` (initialize and tool calls; requested locale), `openai/userAgent` (tool calls; "Optional, best-effort user agent hint"), `openai/userLocation` (tool calls; "Coarse location hint (city, region, country, timezone, longitude, latitude)"), `openai/subject` (tool calls; "Anonymized user id sent to MCP servers for the purposes of rate limiting and identification"), `openai/session` (tool calls; "Anonymized conversation id for correlating tool calls within the same ChatGPT session"). Docs say location and user agent are hints only and servers "must tolerate their absence".
- Also (developers.openai.com/api/docs/mcp): the server gets "whatever data ChatGPT supplies during the interaction", which can include sensitive data a user shared earlier.
- Whether the conversation text is sent beyond the tool arguments: not stated.
- Claude: not stated in official docs (the pages say only that requests come from Anthropic's cloud, that request headers you configure are sent on every request, and that members authenticate separately). The fetch tool also could not confirm identity or conversation fields.

## 8. Facts table
| Fact | Source URL | Read on | Plans |
|---|---|---|---|
| ChatGPT docs now say "as a plugin"; developer mode not mentioned in text | https://developers.openai.com/api/docs/guides/developer-mode | 15 Nov 2026 | not stated |
| Add via Plugins, plus, Add custom MCP server, 7 steps | https://developers.openai.com/api/docs/guides/custom-mcp-server | 15 Nov 2026 | not stated; Business and Enterprise/Edu admin rules below |
| Auth options: OAuth, No authentication, OAuth or no authentication | same | 15 Nov 2026 | not stated |
| Warnings: trust, write confirmation, readOnlyHint, remembered approvals | same | 15 Nov 2026 | not stated |
| Business: admins and owners create and publish; Enterprise/Edu: RBAC; "Create plugins with MCPs" off by default (Enterprise) (search snippets; page returned 403) | https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt and https://help.openai.com/en/articles/20001547-hosting-a-plugin-with-chatgpt-sites | 15 Nov 2026 | Business, Enterprise/Edu |
| ChatGPT widgets run in an iframe via MCP Apps bridge, optional | https://developers.openai.com/apps-sdk/build/chatgpt-ui | 15 Nov 2026 | not stated |
| Review checks UI policy; owner publishes after approval | https://developers.openai.com/apps-sdk/deploy/submission | 15 Nov 2026 | not stated |
| `_meta` fields ChatGPT sends | https://developers.openai.com/plugins/reference | 15 Nov 2026 | not stated |
| Claude custom connector steps, "No sign-in", Free = 1 connector | https://claude.com/docs/connectors/custom/remote-mcp | 15 Nov 2026 | Free, Pro, Max, Ultra, Team, Enterprise |
| Claude Team/Enterprise: Owner adds in Organization settings | same | 15 Nov 2026 | Team, Enterprise |
| Claude connections come from Anthropic cloud; public HTTPS 443 | https://support.claude.com/en/articles/11175166 | 15 Nov 2026 | all |
| Claude interactive connectors, all plans | https://claude.com/blog/interactive-tools-in-claude | 15 Nov 2026 | Free, Pro, Max, Ultra, Team, Enterprise |
| Fuller apps in chat, rolling out, account or org must enable | https://claude.com/blog/interactive-connectors-full-tool | 15 Nov 2026 | all (web, desktop) |
| MCP Apps client list: Claude yes, ChatGPT not listed | https://modelcontextprotocol.io/extensions/apps/overview | 15 Nov 2026 | n/a |

## Still unknown: only testing can answer
- Whether a free or Plus ChatGPT account can see the "Add custom MCP server" button today, and whether developer mode still exists for them.
- Whether a plugin added by one ChatGPT user (unpublished) is usable only by that user (our visitors each add their own) and whether the "No authentication" choice is available on every plan.
- Whether our area-card widget renders in ChatGPT for an unlisted server, and in Claude for a URL-added custom connector.
- Exact `tools/call` payload each host sends today (ChatGPT's `_meta` precision for location, whether Claude sends anything beyond arguments).
- Whether ChatGPT passes the conversation text anywhere beyond the model-chosen tool arguments.
- Claude plan limits on free-plan custom connector count in practice (documented as one).

## Contradictions with our records
1. area-tools.feature (13 Nov) says ChatGPT: "developer mode must be on (Settings, Connectors, Advanced)". Current OpenAI developer docs describe adding a server through **Plugins** ("Add custom MCP server", "Create as a plugin") and do not mention developer mode in their text. The cited URL (developers.openai.com/api/docs/guides/developer-mode) now carries that content. The Settings path and "developer mode" wording need re-checking in the real app.
2. 0056 says "ChatGPT allowed a connection with no sign-in only in developer mode". Current docs list "No authentication" as an ordinary authentication option on the add-server screen, with no developer-mode condition stated.
3. area-tools.feature says "on work plans an admin must allow developer mode first". Current help-centre snippets name the permission "Create plugins with MCPs" (Business: admins and owners only; Enterprise/Edu: RBAC; off by default in Enterprise).
4. Consistent with our records: Claude "No sign in" (now spelled "No sign-in"), Free plan one custom connector, MCP Apps list includes Claude and not ChatGPT. ChatGPT docs now do say widgets use the MCP Apps standard (`_meta.ui.resourceUri`), which supports 0037's cited statement.
5. 0056 says the page must explain that the host app sees what it sends. Confirmed, with extra detail: ChatGPT sends anonymised user and conversation ids and a coarse location hint (section 7). Our privacy notice and "no visitor input in any log" rule (0014, 0053) should say we do not store `openai/subject`, `openai/session` or `openai/userLocation`, or decide whether to use `openai/subject` for rate limiting (OpenAI offers it for exactly that). area-tools.feature line 36 says hosts are identified by anonymised network address only; OpenAI documents `openai/subject` as a rate-limit identifier, so that is an option, not a contradiction.

## Controller check (15 Nov 2026)
Re-read https://developers.openai.com/plugins/reference directly. Besides `openai/subject` ("Anonymized user id sent to MCP servers for the purposes of rate limiting and identification"), `openai/session` ("Anonymized conversation id …") and `openai/userLocation` ("Coarse location hint (`city`, `region`, `country`, `timezone`, `longitude`, `latitude`)"), ChatGPT also sends `openai/organization` ("Anonymized organization id …, when available"), `openai/userAgent` ("Optional, best-effort user agent hint") and `openai/locale`. The page says `userAgent` and `userLocation` "are hints only; servers should never rely on them for authorization decisions and must tolerate their absence."
