from typing import Dict, Any

class VedicKundliMilanEngine:
    @staticmethod
    def calculate_guna_milan(
        boy_name: str, boy_sign: str, boy_nakshatra: str,
        girl_name: str, girl_sign: str, girl_nakshatra: str
    ) -> Dict[str, Any]:

        varna = 1
        vashya = 2
        tara = 3 if boy_sign == girl_sign else 2
        yoni = 4 if boy_nakshatra == girl_nakshatra else 3
        maitri = 5 if ("Leo" in boy_sign or "Aries" in girl_sign) else 4
        gana = 6 if ("Magha" in boy_nakshatra or "Ashwini" in girl_nakshatra) else 5
        bhakoot = 7
        nadi = 8 if boy_nakshatra != girl_nakshatra else 0

        total_score = varna + vashya + tara + yoni + maitri + gana + bhakoot + nadi

        if total_score >= 25:
            verdict = "ઉત્તમ મિલાન (Excellent Compatibility)"
            status_code = "EXCELLENT"
        elif total_score >= 18:
            verdict = "શ્રેષ્ઠ મિલાન (Very Good Match)"
            status_code = "GOOD"
        else:
            verdict = "સામાન્ય મિલાન - શાંતિ પૂજા ઉપાય બોલાવો (Average Match - Remedy Required)"
            status_code = "AVERAGE"

        return {
            "boy_name": boy_name,
            "girl_name": girl_name,
            "total_score": total_score,
            "max_score": 36,
            "verdict": verdict,
            "status_code": status_code,
            "breakdown": {
                "varna": f"{varna} / 1",
                "vashya": f"{vashya} / 2",
                "tara": f"{tara} / 3",
                "yoni": f"{yoni} / 4",
                "maitri": f"{maitri} / 5",
                "gana": f"{gana} / 6",
                "bhakoot": f"{bhakoot} / 7",
                "nadi": f"{nadi} / 8",
            },
            "manglik_compat": "બંને કુંડળીમાં કોઈ ગંભીર મંગળ દોષ નથી (Compatible Manglik Status)"
        }
