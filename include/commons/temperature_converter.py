def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def fahrenheit_to_kelvin(fahrenheit):
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))

def kelvin_to_fahrenheit(kelvin):
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))

def main():
    print("Temperature Converter")
    print("Choose the conversion you want to perform:")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Fahrenheit to Kelvin")
    print("6. Kelvin to Fahrenheit")
    
    choice = input("Enter your choice (1-6): ")
    
    if choice == '1':
        celsius = float(input("Enter temperature in Celsius: "))
        print(f"{celsius} °C is {celsius_to_fahrenheit(celsius)} °F")
    
    elif choice == '2':
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        print(f"{fahrenheit} °F is {fahrenheit_to_celsius(fahrenheit)} °C")
    
    elif choice == '3':
        celsius = float(input("Enter temperature in Celsius: "))
        print(f"{celsius} °C is {celsius_to_kelvin(celsius)} K")
    
    elif choice == '4':
        kelvin = float(input("Enter temperature in Kelvin: "))
        print(f"{kelvin} K is {kelvin_to_celsius(kelvin)} °C")
    
    elif choice == '5':
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        print(f"{fahrenheit} °F is {fahrenheit_to_kelvin(fahrenheit)} K")
    
    elif choice == '6':
        kelvin = float(input("Enter temperature in Kelvin: "))
        print(f"{kelvin} K is {kelvin_to_fahrenheit(kelvin)} °F")
    
    else:
        print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
