from typing import Dict, Any

class NumerologyEngine:
    @staticmethod
    def reduce_number(num: int) -> tuple[int, str]:
        """Reduces a number to a single digit and returns the calculation string."""
        if num < 10:
            return num, str(num)
        
        calc_steps = [str(num)]
        current = num
        while current >= 10:
            digits = [int(d) for d in str(current)]
            current = sum(digits)
            calc_steps.append(f"{' + '.join(map(str, digits))} = {current}")
            
        return current, " -> ".join(calc_steps)

    @staticmethod
    def calculate_destiny(dob: str, name: str) -> Dict[str, Any]:
        # DOB expected in YYYY-MM-DD or DD/MM/YYYY. Let's assume YYYY-MM-DD for consistency with Kundli API
        # but handle DD/MM/YYYY just in case
        parts = dob.replace('/', '-').split('-')
        if len(parts) == 3:
            if len(parts[0]) == 4: # YYYY-MM-DD
                year, month, day = parts[0], parts[1], parts[2]
            else: # DD-MM-YYYY
                day, month, year = parts[0], parts[1], parts[2]
        else:
            day, month, year = "16", "5", "1998"
            
        # 1. Mulank (Root/Birth Number) -> Sum of day digits
        day_sum = sum(int(d) for d in day if d.isdigit())
        mulank, mulank_calc = NumerologyEngine.reduce_number(day_sum)
        mulank_calc = f"{day} -> {mulank_calc}" if int(day) >= 10 else f"{day} = {mulank}"
        
        # 2. Bhagyank (Life Path Number) -> Sum of all DOB digits
        dob_digits = [int(d) for d in f"{day}{month}{year}" if d.isdigit()]
        dob_digits_sum = sum(dob_digits)
        bhagyank, bhagyank_calc = NumerologyEngine.reduce_number(dob_digits_sum)
        bhagyank_calc = f"જન્મતારીખનો સરવાળો ({' + '.join(map(str, dob_digits))} = {dob_digits_sum})\n{bhagyank_calc}"
        
        # 3. Namank (Destiny Number) -> Sum of letters
        # Pythagorean system: A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9, J=1...
        letter_values = {
            'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9,
            'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9,
            'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8
        }
        
        name_clean = "".join(c for c in name.upper() if c.isalpha())
        
        soul_urge_sum = 0
        personality_sum = 0
        hidden_passion_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
        
        if name_clean:
            name_sum = sum(letter_values.get(c, 0) for c in name_clean)
            
            # Create letter breakdowns
            all_letters_calc = " + ".join([f"{c}({letter_values.get(c, 0)})" for c in name_clean])
            vowels_calc = " + ".join([f"{c}({letter_values.get(c, 0)})" for c in name_clean if c in ['A', 'E', 'I', 'O', 'U']])
            cons_calc = " + ".join([f"{c}({letter_values.get(c, 0)})" for c in name_clean if c not in ['A', 'E', 'I', 'O', 'U']])
            
            namank, namank_calc = NumerologyEngine.reduce_number(name_sum)
            namank_calc = f"નામના બધા અક્ષરો: {all_letters_calc} = {name_sum}\n{namank_calc}"
            
            for c in name_clean:
                val = letter_values.get(c, 0)
                if val > 0:
                    hidden_passion_counts[val] += 1
                if c in ['A', 'E', 'I', 'O', 'U']:
                    soul_urge_sum += val
                else:
                    personality_sum += val
                    
            soul_urge, soul_urge_calc = NumerologyEngine.reduce_number(soul_urge_sum)
            if vowels_calc:
                soul_urge_calc = f"સ્વરો (Vowels): {vowels_calc} = {soul_urge_sum}\n{soul_urge_calc}"
            else:
                soul_urge_calc = f"નામમાં કોઈ સ્વર નથી.\n{soul_urge_calc}"
            
            personality, personality_calc = NumerologyEngine.reduce_number(personality_sum)
            if cons_calc:
                personality_calc = f"વ્યંજનો (Consonants): {cons_calc} = {personality_sum}\n{personality_calc}"
            else:
                personality_calc = f"નામમાં કોઈ વ્યંજન નથી.\n{personality_calc}"
            
            hidden_passion = max(hidden_passion_counts, key=hidden_passion_counts.get)
            hidden_passion_calc = f"અંક {hidden_passion} નામમાં સૌથી વધુ વખત આવે છે"
            
        else:
            namank, namank_calc = 1, "નામ આપેલ નથી"
            soul_urge, soul_urge_calc = 1, "નામ આપેલ નથી"
            personality, personality_calc = 1, "નામ આપેલ નથી"
            hidden_passion, hidden_passion_calc = 1, "નામ આપેલ નથી"

        meanings = {
            1: "Leader, independent, original, and confident.",
            2: "Peacemaker, diplomatic, sensitive, and cooperative.",
            3: "Creative, sociable, expressive, and optimistic.",
            4: "Practical, hardworking, disciplined, and organized.",
            5: "Freedom-loving, adventurous, adaptable, and dynamic.",
            6: "Nurturing, responsible, loving, and family-oriented.",
            7: "Analytical, spiritual, intuitive, and philosophical.",
            8: "Ambitious, powerful, business-minded, and authoritative.",
            9: "Humanitarian, compassionate, selfless, and globally aware."
        }

        return {
            "mulank": {
                "number": mulank,
                "title": "મૂલાંક",
                "calculation": mulank_calc,
                "meaning": meanings.get(mulank, "")
            },
            "bhagyank": {
                "number": bhagyank,
                "title": "ભાગ્યાંક (Life Path Number)",
                "calculation": bhagyank_calc,
                "meaning": meanings.get(bhagyank, "")
            },
            "namank": {
                "number": namank,
                "title": "નામાંક (Destiny Number)",
                "calculation": namank_calc,
                "meaning": meanings.get(namank, "")
            },
            "soul_urge": {
                "number": soul_urge,
                "title": "સોલ અર્જ (Soul Urge Number)",
                "calculation": soul_urge_calc,
                "meaning": meanings.get(soul_urge, "")
            },
            "personality": {
                "number": personality,
                "title": "પર્સનાલિટી (Personality Number)",
                "calculation": personality_calc,
                "meaning": meanings.get(personality, "")
            },
            "hidden_passion": {
                "number": hidden_passion,
                "title": "હિડન પેશન (Hidden Passion Number)",
                "calculation": hidden_passion_calc,
                "meaning": meanings.get(hidden_passion, "")
            },
            "lucky_numbers": [mulank, (bhagyank + mulank) % 9 or 9],
            "lucky_colors": ["White", "Yellow", "Blue"] if mulank % 2 == 0 else ["Red", "Orange", "Gold"]
        }
