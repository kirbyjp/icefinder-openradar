import math

class IceRadarDefragmenter:
    def __init__(self, freezing_level_ft=12000, lapse_rate_ft_deg=1000):
        """
        Initializes the software-defined stretching engine.
        freezing_level_ft: Estimated or sensor-fed 0-degree Celsius altitude.
        """
        self.freezing_level_ft = freezing_level_ft
        
        # Reflectivity constants (Ice reflects ~1/20th of liquid water)
        self.ICE_REFLECTIVITY_FACTOR = 20.0 
        
        # Raw radar signal thresholds (Standard dBZ approximations)
        self.DBZ_NOISE_FLOOR = 15.0
        self.DBZ_LIGHT_RAIN = 20.0

    def calculate_beam_altitude(self, aircraft_alt_ft, distance_nm, tilt_deg):
        """
        Uses basic trigonometry to calculate the exact altitude of the radar beam 
        at a specific distance milestone ahead of the aircraft.
        """
        # Convert nautical miles to feet (1 NM ≈ 6076.12 feet)
        distance_ft = distance_nm * 6076.12
        tilt_rad = math.radians(tilt_deg)
        
        # Geometric height displacement
        height_delta_ft = distance_ft * math.sin(tilt_rad)
        
        # Total altitude of the target slice
        return aircraft_alt_ft + height_delta_ft

    def process_radar_return(self, raw_dbz, target_altitude_ft, user_bias=1.0):
        """
        Processes raw reflectivity. If the beam is slicing above the freezing level,
        it stretches weak signals based on a base multiplier combined with a user-adjustable bias.
        
        user_bias: Float value (e.g., 0.5 to 2.0). 
                   Values below 1.0 attenuate/dim down the ice overlay (clean up noise).
                   Values above 1.0 amplify/increase sensitivity to capture micro-returns.
        """
        # If the signal is pure static/noise floor, leave it clean to prevent ghosting
        if raw_dbz < self.DBZ_NOISE_FLOOR:
            return {"mode": "CLEAN", "render_color": "TRANSPARENT"}

        # Check if the radar beam is operating in the sub-zero Icing Zone
        if target_altitude_ft >= self.freezing_level_ft:
            
            # If it looks like harmless light rain aloft, it is likely massive dry ice
            if raw_dbz <= self.DBZ_LIGHT_RAIN:
                
                # Dynamic visual stretching factoring in the pilot's sensitivity bias knob
                effective_multiplier = self.ICE_REFLECTIVITY_FACTOR * user_bias
                amplified_dbz = raw_dbz * effective_multiplier
                
                # Flag the UI to use the interleaved/checkered paint mode
                return {
                    "mode": "INTERLEAVED_ICE_WARNING",
                    "original_dbz": raw_dbz,
                    "amplified_dbz": amplified_dbz,
                    "applied_multiplier": effective_multiplier,
                    "render_style": "CHECKERED_CYAN_GREEN"
                }
                
        # Otherwise, process and display weather via standard legacy rules
        return {"mode": "STANDARD_RAIN", "render_color": "STANDARD_PALETTE"}

# --- QUICK PROOF OF CONCEPT VALIDATION ---
if __name__ == "__main__":
    engine = IceRadarDefragmenter(freezing_level_ft=10000)
    
    # Scenario: Aircraft at 15,000ft cruising altitude, looking 20 miles out
    # at a tilt angle of -2 degrees. A weak 18 dBZ signal is detected.
    beam_alt = engine.calculate_beam_altitude(aircraft_alt_ft=15000, distance_nm=20, tilt_deg=-2.0)
    result = engine.process_radar_return(raw_dbz=18.0, target_altitude_ft=beam_alt)
    
    print(math.floor(beam_alt))
    print(result)
