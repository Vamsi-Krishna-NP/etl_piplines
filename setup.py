from setuptools import setup, find_packages

def get_requirements() -> list[str]:
    """
    Reads the requirements from the requirements.txt file and returns a list of requirements.
    Returns:
        list[str]: _description_
    """
    
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
    
setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Vamsi Krishna',
    author_email='mr.vkjilla2024@gmail.com',
    packages= find_packages(),
    install_requires= get_requirements(),
    )