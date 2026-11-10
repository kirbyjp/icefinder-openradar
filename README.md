# IceFinder OpenRadar 🛰️❄️

**IceFinder OpenRadar** is an open-source, software-defined aviation weather radar enhancement engine. By leveraging an aircraft's existing nose-cone radar hardware, barometric altitude, and antenna tilt geometry, IceFinder OpenRadar mathematically isolates and amplifies the weak signals characteristic of high-altitude clear ice and dry hail crystals.

This project is released entirely for free under the **MIT License**. It exists to democratize flight safety, eliminate corporate technical gridlock, and prevent future inflight icing tragedies.

---

## The Problem: The Radar "Ice Blindness"
Standard airborne weather radar operates on radio wave reflectivity, which is highly dependent on liquid water. Frozen ice crystals have a dielectric constant that results in a reflectivity deficit of **1/5th to 1/20th (roughly 20 times less) compared to liquid rain**.

As a result, a rapidly building convective storm cell at high altitudes can be packed with severe clear ice or dry hail while appearing as a completely harmless, light green cloud on a standard cockpit display. Entering these zones can result in instantaneous, catastrophic ice accumulation and aerodynamic stall—as heavily scrutinized in recent high-altitude aviation accidents, including the tragic Learjet 60 crash in Palm Beach, Florida.

---

## The Solution: Software Geometry & Visual Stretching
An aircraft can solve this problem entirely in software through **Altitude-Dependent Automated Gain Control (AGC)** and **Spatial Dithering (Interleaved UI)** without expensive hardware retrofits.

The core filtering logic relies on a three-stage processing pipeline:

* **Stage 1: Input Collection:** The software continuously captures the raw radar return along with the aircraft's current barometric altitude and active antenna tilt angle.
* **Stage 2: Geometric Isothermal Filtering:** It maps the tilt geometry to calculate the exact altitude of the radar slice using the formula: Target Altitude = Aircraft Altitude + (Distance to Storm * sin(Antenna Tilt Angle)).
* **Stage 3: Thermal Decision Core:** The software compares the target slice altitude against the known freezing level. If the beam is operating below the freezing level, the data passes through legacy rules unchanged. If the beam is operating above the freezing level, a 20x visual stretch is automatically applied to weak signals, flagging those pixels to render with a checkered, interleaved UI overlay instead of a solid legacy color palette.

---

## Legal Status: Defensive Prior Art
This repository, its underlying algorithms, mathematical formulas, and UI presentation methodologies are published openly and globally as of **November 2026**.

This public disclosure serves as **Defensive Prior Art**. Under global patent laws (including AIA 35 U.S.C. § 102 in the United States), the publication of this code explicitly blocks any corporation, entity, or individual from claiming proprietary patent rights over this specific methodology of software-defined, altitude-geometric radar stretching and interleaved texture rendering. **It is, and will forever remain, a free safety standard for all of humanity.**

---

## How to Get Involved
* **Avionics & Simulation Devs:** Pull the core mathematical engine from `ice_radar_logic.py` and implement it into open-source Electronic Flight Bags (EFBs) or flight simulation environments (X-Plane / MSFS).
* **UI/UX Engineers:** Help us optimize the canvas-rendering scripts to ensure the checkered patterns remain completely clear, artifact-free, and legible on low-resolution legacy displays under high-vibration/turbulent conditions.

---

## License
Distributed under the MIT License. See `LICENSE` for more information.
