from setuptools import setup, find_packages

def get_requirements() -> list[str]:
    requirements_lst = []
    
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement= line.strip()
                if requirement and requirement not in ('-e .', '-r requirements.txt'):
                    requirements_lst.append(requirement)
        
                    
    except FileNotFoundError:
        print("requirements.txt not found. Please ensure it exists in the project root.")
        
    return requirements_lst
    
print(get_requirements())