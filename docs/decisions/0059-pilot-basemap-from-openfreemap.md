# 0059: The pilot's basemap comes from OpenFreeMap's public servers

**ID:** DA-37  
**Status:** Accepted (founder, 19 Nov 2026, two prompt windows: "Use their public servers", then "OpenFreeMap (Recommended)")  
**Date:** 2026-11-19  
**Stage:** 5b (the pilot)  
**Amends (no older text is rewritten):** register line DA-25 ("OpenStreetMap, self-hosted") and the reason in FE-03 ("no other company sees which streets a visitor looks at"), for the pilot only. [0014](0014-privacy-and-data-protection.md) stands: a map view sends the visitor's IP address to a company, so the privacy notice names it.

## Context
The pilot's area maps and the 2D street map need a basemap, the background of streets, buildings and water that our places are drawn on. DA-25 (16 Nov 2026) chose OpenStreetMap tiles that we store and serve ourselves, with the price and the running cost (IN-02) still pending. A tile is one small square of the map; a basemap is many tiles. A map library (here MapLibre, `maplibre-gl`, already approved) fetches the tiles it needs for the area on screen, so whoever serves them sees each request. On 19 Nov 2026 the founder was asked how the pilot should get its tiles.

## Options
Facts checked on 19 Nov 2026 (the pages' own words, in quotes):
### Option A: OpenFreeMap's public tile servers (chosen)
[openfreemap.org](https://openfreemap.org/): OpenStreetMap vector tiles in the OpenMapTiles schema, which MapLibre reads. Free, with "no limits on the number of map views or requests"; "no registration, no user database, no API keys, and no cookies". Commercial use is allowed. Attribution is required (OpenMapTiles and OpenStreetMap; MapLibre adds it). The operator says "I don't offer SLA guarantees". Privacy policy, read 19 Nov 2026 ([openfreemap.org/privacy](https://openfreemap.org/privacy/)): "We do not use cookies or tracking technologies"; "We do not store IP addresses in our access logs"; "If the server encounters an error, the error log may include the IP address and requested URL"; "we may temporarily enable IP logging for a maximum of 30 days to investigate and resolve the issue"; "All server logs are automatically deleted after 7 days, except logs collected during security incidents, which are deleted after a maximum of 30 days"; "We may use Cloudflare as a CDN to improve service delivery. Cloudflare may collect certain information as described in their privacy policy." Terms, read 19 Nov 2026 ([openfreemap.org/tos](https://openfreemap.org/tos/)): "We aim to maintain the Site’s availability but may discontinue it at any time without notice."
### Option B: Stadia Maps
[Pricing](https://stadiamaps.com/pricing/) (read 19 Nov 2026). Its free tier says "Commercial use not allowed", so a commercial product needs Starter, $20 a month.
### Option C: MapTiler
[Pricing](https://www.maptiler.com/cloud/pricing/) (read 19 Nov 2026). The free plan gives 5,000 sessions and is "Suitable for testing, PoC, prototyping, personal, or non-commercial use" (read 19 Nov 2026); Flex is $30 a month.
### Option D: Protomaps' hosted tiles
[protomaps.com](https://protomaps.com/) (read 19 Nov 2026). "Noncommercial use is free", so not for a commercially viable product.
### Option E: the OpenStreetMap public tile servers
Ruled out in `docs/references/data-sources.md` (donation-funded, no SLA, can be blocked without notice, not for production).
### Option F: self-hosting (DA-25's plan)
Serve our own tiles from OpenFreeMap's weekly PMTiles files (a single-file tile format). Keeps the visitor's map views private, but has a hosting cost and work (IN-02), so it is the exit rather than the start.

## Recommendation
The agent first recommended using OpenStreetMap as the tile source and pricing it at stage 5b. After the founder chose public servers, the agent recommended OpenFreeMap: the only free public option that allows commercial use, with no limits, no key and no cookies, and with self-hosting as the exit.

## Decision
The founder chose, in two prompt windows on 19 Nov 2026: "Use their public servers" (over "As tile source, price at 5b (Recommended)" and "Research and price now"), then "OpenFreeMap (Recommended)" (over "Stadia Maps Starter" and "MapTiler Flex"). This is the first use of the founder's "free first, within the rules" rule, recorded as register line WW-22 (founder, 19 Nov 2026).

## Consequences
- **Privacy:** each map view sends OpenFreeMap (and Cloudflare, which its policy says it may use as a CDN) the visitor's IP address and the tiles for the area on screen. The map opens centred on the postcode that was checked, at street level, so the tile requests show roughly where the visitor is looking; 0014 treats that as potentially personal data. The privacy notice names both (`pilot/public-pages.feature` PRIV-18) and may quote OpenFreeMap's stated practice above, attributed to its policy. What stays a placeholder is our lawful basis and retention wording (SE-02). The policy and terms are read here, but **before launch** they are read again, because they can change. The reason FE-03 gave ("no other company sees which streets a visitor looks at") no longer holds for the pilot, and benchmark B28 ("no third-party request without the visitor's action") no longer holds for maps: the map loads with the result. Loading the map only when the visitor asks is a possible change, listed under "Open to the founder" below.
- **If its servers fail:** the map shows a plain "map unavailable" state and every fact still shows in its list and its topic (rule 7, [0029](0029-external-services.md); MAP-27). There is no SLA, and the terms say OpenFreeMap "may discontinue it at any time without notice", so this will happen sometimes and could become permanent; the MAP-27 fallback covers both, and self-hosting is the exit.
- **Which maps:** every pilot map, including City Explorer's (0055 makes City Explorer part of the pilot). This is the agent's reading, open to the founder. CITY-89, CITY-104, HOOD-27 and HOOD-39 and the City Explorer design (§68, §172, dated notes) are amended to say so; its boundary files, fonts and chart library stay on our hosting.
- **Cost:** no tile-hosting cost in IN-02 for the pilot.
- **Attribution:** OpenMapTiles and OpenStreetMap are credited on the map (MAP-18); MapLibre adds it.
- **Rule:** the choice follows "free first, within the rules" (WW-22).
- **Revisit** if OpenFreeMap changes its terms, if its reliability is poor, or before a commercial launch. The exit is self-hosting from its weekly PMTiles files (DA-25's plan).

## Amended 19 Nov 2026
The founder chose, in a prompt window, "Load when opened" (over the agent's "Load with the result (Recommended)"): every pilot map shows a "Show map" control and nothing is requested from OpenFreeMap until the visitor taps it (register line FE-75; MAP-28 to MAP-30). So B28 holds until the visitor chooses, and the Privacy notice says map data is requested only when the visitor chooses "Show map" (PRIV-18). The choice is not remembered; that is the agent's call, open to the founder. The Privacy and benchmark B28 lines above describe what happens once the map is shown.
