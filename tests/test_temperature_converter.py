import pytest
from include.commons.temperature_converter import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    celsius_to_kelvin,
    kelvin_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_to_fahrenheit,
)

def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert pytest.approx(celsius_to_fahrenheit(25), 0.1) == 77

def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(32) == 0
    assert fahrenheit_to_celsius(212) == 100
    assert pytest.approx(fahrenheit_to_celsius(77), 0.1) == 25

def test_celsius_to_kelvin():
    assert celsius_to_kelvin(0) == 273.15
    assert celsius_to_kelvin(100) == 373.15
    assert pytest.approx(celsius_to_kelvin(25), 0.01) == 298.15

def test_kelvin_to_celsius():
    assert kelvin_to_celsius(273.15) == 0
    assert kelvin_to_celsius(373.15) == 100
    assert pytest.approx(kelvin_to_celsius(298.15), 0.01) == 25

def test_fahrenheit_to_kelvin():
    assert pytest.approx(fahrenheit_to_kelvin(32), 0.01) == 273.15
    assert pytest.approx(fahrenheit_to_kelvin(212), 0.01) == 373.15
    assert pytest.approx(fahrenheit_to_kelvin(77), 0.01) == 298.15

def test_kelvin_to_fahrenheit():
    assert pytest.approx(kelvin_to_fahrenheit(273.15), 0.01) == 32
    assert pytest.approx(kelvin_to_fahrenheit(373.15), 0.01) == 212
    assert pytest.approx(kelvin_to_fahrenheit(298.15), 0.01) == 77
