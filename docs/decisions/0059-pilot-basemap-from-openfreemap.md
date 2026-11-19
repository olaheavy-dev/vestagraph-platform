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
[openfreemap.org](https://openfreemap.org/): OpenStreetMap vector tiles in the OpenMapTiles schema, which MapLibre reads. Free, with "no limits on the number of map views or requests"; "no registration, no user database, no API keys, and no cookies". Commercial use is allowed. Attribution is required (OpenMapTiles and OpenStreetMap; MapLibre adds it). The operator says "I don't offer SLA guarantees". Whether it logs IP addresses is not stated.
### Option B: Stadia Maps
Its free tier says "Commercial use not allowed", so a commercial product needs Starter, $20 a month.
### Option C: MapTiler
The free plan gives 5,000 sessions; Flex is $30 a month.
### Option D: Protomaps' hosted tiles
"Noncommercial use is free", so not for a commercially viable product.
### Option E: the OpenStreetMap public tile servers
Ruled out in `docs/references/data-sources.md` (donation-funded, no SLA, can be blocked without notice, not for production).
### Option F: self-hosting (DA-25's plan)
Serve our own tiles from OpenFreeMap's weekly PMTiles files (a single-file tile format). Keeps the visitor's map views private, but has a hosting cost and work (IN-02), so it is the exit rather than the start.

## Recommendation
The agent first recommended using OpenStreetMap as the tile source and pricing it at stage 5b. After the founder chose public servers, the agent recommended OpenFreeMap: the only free public option that allows commercial use, with no limits, no key and no cookies, and with self-hosting as the exit.

## Decision
The founder chose, in two prompt windows on 19 Nov 2026: "Use their public servers" (over "As tile source, price at 5b (Recommended)" and "Research and price now"), then "OpenFreeMap (Recommended)" (over "Stadia Maps Starter" and "MapTiler Flex").

## Consequences
- **Privacy:** OpenFreeMap receives each map view's IP address and the map area being viewed, so the privacy notice names it (`pilot/public-pages.feature` PRIV-18). The notice cannot say how long OpenFreeMap keeps IP addresses: its page does not say. **Before launch**, read OpenFreeMap's terms of service and confirm its IP logging; until then the notice says what is decided and leaves the rest as a placeholder (SE-02). The reason FE-03 gave ("no other company sees which streets a visitor looks at") no longer holds for the pilot.
- **If its servers fail:** the map shows a plain "map unavailable" state and every fact still shows in its list and its topic (rule 7, [0029](0029-external-services.md); MAP-27). There is no SLA, so this will happen sometimes.
- **Cost:** no tile-hosting cost in IN-02 for the pilot.
- **Attribution:** OpenMapTiles and OpenStreetMap are credited on the map (MAP-18); MapLibre adds it.
- **Revisit** if OpenFreeMap changes its terms, if its reliability is poor, or before a commercial launch. The exit is self-hosting from its weekly PMTiles files (DA-25's plan).
