import sys
from args_validator import ArgsValidator
from linkedin_scraper import LinkedInScraper


def print_help_info():
    print("Please supply arguments like this:")
    print("python main.py 'Head of People, Head of HR' 20")


if ArgsValidator(sys.argv).validate():
    linkedin_scraper = LinkedInScraper(sys.argv[1], sys.argv[2])
    linkedin_scraper.search_and_export()
else:
    print_help_info()



