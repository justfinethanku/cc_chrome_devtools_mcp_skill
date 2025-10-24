# Core Web Vitals Metrics Reference

**Last Updated:** October 2024
**Source:** web.dev official documentation
**Format:** Mike Dion's Markdown (.md) - keeping documentation clear since its creation

---

## Overview

Core Web Vitals are Google's standardized metrics for measuring user experience on the web. All three metrics must meet "good" thresholds at the **75th percentile** of page loads to pass.

---

## Official Core Web Vitals (3 Metrics)

### 1. Interaction to Next Paint (INP)

**Status:** Active Core Web Vital (replaced FID on March 12, 2024)

**Definition:** Assesses page's overall responsiveness by observing latency of all click, tap, and keyboard interactions. Reports the longest interaction duration (with outliers removed for high-interaction pages).

**What it measures:**
- Input delay (time from user action to event handler start)
- Processing time (event handler execution)
- Presentation delay (rendering the next frame)

**Thresholds:**
- **Good:** ≤ 200ms
- **Needs Improvement:** 200-500ms
- **Poor:** > 500ms

**Measurement:** Requires field data (real user interactions)

---

### 2. Largest Contentful Paint (LCP)

**Definition:** Loading performance metric marking when page's main content has likely loaded. Reports render time of largest image or text block visible in viewport.

**Elements measured:**
- `<img>` elements
- `<image>` elements inside `<svg>`
- `<video>` elements (poster image)
- Elements with CSS background images
- Block-level text elements

**Thresholds:**
- **Good:** ≤ 2.5 seconds
- **Needs Improvement:** 2.5-4 seconds
- **Poor:** > 4 seconds

**Measurement:** Available in both field and lab data

---

### 3. Cumulative Layout Shift (CLS)

**Definition:** Visual stability metric quantifying unexpected layout shifts during entire page lifecycle. Measures largest burst of layout shift scores.

**Common causes:**
- Images without explicit dimensions
- Dynamically injected content (ads, embeds)
- Web fonts causing FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text)
- Third-party widgets

**Thresholds:**
- **Good:** ≤ 0.1
- **Needs Improvement:** 0.1-0.25
- **Poor:** > 0.25

**Measurement:** Available in both field and lab data

---

## Total Blocking Time (TBT)

**Status:** NOT a Core Web Vital - Lab proxy metric only

**Definition:** Lab-only metric measuring total time after First Contentful Paint (FCP) where main thread was blocked (>50ms) preventing input responsiveness.

**Threshold:**
- **Good:** < 200ms (on average mobile hardware)

**Relationship to INP:**
- Used as lab proxy for INP (cannot measure INP without real user interactions)
- TBT improvements often correlate with INP improvements
- **Important:** TBT is not a substitute for INP
- May flag potential problems that don't affect real users
- Cannot capture interaction issues outside lab test scenarios

**Official guidance:** "TBT may be a reasonable proxy metric for INP for the lab but it's not a substitute for INP in and of itself."

---

## INP Transition Timeline

The transition from First Input Delay (FID) to INP as a Core Web Vital:

- **May 2022:** INP introduced as experimental metric
- **May 2023:** INP promoted to pending Core Web Vital
- **January 31, 2024:** Official announcement of March 12 transition date
- **March 12, 2024:** INP replaced FID as stable Core Web Vital
- **March 12, 2024:** FID removed from Google Search Console
- **September 12, 2024:** FID removed from other Google tools (6-month deprecation period completed)

---

## Field vs Lab Data

### Field Data (Real User Monitoring)

**Characteristics:**
- Collected from actual users in real-world conditions
- Reflects diverse device capabilities, network conditions, and user interactions
- **Used by Google for search rankings**
- Updated every 28 days in Chrome User Experience Report (CrUX)
- Can measure all three Core Web Vitals including INP

**Data sources:**
- Chrome User Experience Report (CrUX)
- Real User Monitoring (RUM) tools
- PageSpeed Insights field data
- Search Console Core Web Vitals report

---

### Lab Data (Synthetic Monitoring)

**Characteristics:**
- Controlled environment with predefined conditions
- Consistent and reproducible results
- Ideal for debugging and pre-production testing
- **Not used for search rankings**
- Cannot measure INP (requires real user interactions)
- Uses TBT as proxy for responsiveness

**Data sources:**
- Lighthouse audits
- Chrome DevTools Performance panel
- WebPageTest
- PageSpeed Insights lab data

---

## Evaluation Standard

### 75th Percentile Rule

Core Web Vitals are evaluated at the **75th percentile** of page loads, meaning:
- 75% of visits to your site must meet the "good" threshold
- This ensures most users have a good experience
- Applied separately to each metric (INP, LCP, CLS)
- Calculated from field data over rolling 28-day period

### Why 75th percentile?

- Balances between median (50th) and extreme outliers (95th+)
- Accounts for variability in real-world conditions
- Provides actionable target that's achievable for most sites
- Used consistently across all Core Web Vitals metrics

---

## Key Insights

1. **Field data trumps lab data:** Only field data affects search rankings and represents actual user experience.

2. **INP requires real interactions:** You cannot measure INP in lab environments; use TBT as a directional indicator during development.

3. **All three metrics matter:** Sites must pass all three Core Web Vitals thresholds, not just one or two.

4. **75th percentile is the standard:** Meeting thresholds for only 50% of users is insufficient.

5. **TBT is a helper, not a goal:** Optimize for INP in the field; use TBT to catch issues early in development.

---

## Additional Resources

- **Web Vitals Overview:** https://web.dev/articles/vitals
- **INP Documentation:** https://web.dev/articles/inp
- **LCP Documentation:** https://web.dev/articles/lcp
- **CLS Documentation:** https://web.dev/articles/cls
- **TBT Documentation:** https://web.dev/articles/tbt
- **Lab vs Field Data:** https://web.dev/articles/lab-and-field-data-differences
- **INP Launch Announcement:** https://web.dev/blog/inp-cwv-launch
- **PageSpeed Insights:** https://pagespeed.web.dev
