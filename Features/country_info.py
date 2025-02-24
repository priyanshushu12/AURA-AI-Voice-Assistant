import requests

def get_country_info(country_name):
    # REST Countries API URL to fetch country details
    url = f"https://restcountries.com/v3.1/name/{country_name}"

    try:
        response = requests.get(url)
        data = response.json()  # Parse the response JSON
        
        if response.status_code == 200 and data:
            country = data[0]  # The first country in the list
            country_name = country['name']['common']
            capital = country.get('capital', ['N/A'])[0]
            population = country.get('population', 'N/A')
            area = country.get('area', 'N/A')
            currencies = ', '.join([currency for currency in country.get('currencies', {}).keys()])
            languages = ', '.join([language for language in country.get('languages', {}).values()])
            region = country.get('region', 'N/A')
            subregion = country.get('subregion', 'N/A')

            # Return the country information as a string
            return (f"Country: {country_name}\n"
                    f"Capital: {capital}\n"
                    f"Population: {population}\n"
                    f"Area: {area} km²\n"
                    f"Currencies: {currencies}\n"
                    f"Languages: {languages}\n"
                    f"Region: {region}\n"
                    f"Subregion: {subregion}")
        else:
            return f"Country {country_name} not found."
    
    except Exception as e:
        return f"An error occurred: {e}"

def get_country_info_from_user():
    # Prompt the user to input the country name
    country_name = input("Enter the name of the country: ").lower()

    # Call the function to display the country data
    country_info = get_country_info(country_name)
    print(country_info)
    return country_info
