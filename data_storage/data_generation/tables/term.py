import random

def generate_fake_terms(n_years=5, start_year=2018):
    term_list = []
    generated_codes = set()
    current_year = start_year
    code_counter = 180 

    for _ in range(n_years):
        for order in [1, 2]: 
            while True:
                term_code = str(code_counter)
                if term_code not in generated_codes:
                    generated_codes.add(term_code)
                    break
                code_counter += 1 
                
            term_name = f"{current_year}-{current_year + 1}"
            term = {
                "term_code": term_code,
                "term_name": term_name,
                "order": order
            }
            term_list.append(term)
            code_counter += 1 
            
        current_year += 1 

    return term_list
