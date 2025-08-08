import sys
from pkg.calculator import Calculator

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py '<expression>'")
        sys.exit(1)
    
    expression = sys.argv[1]
    calculator = Calculator()
    result = calculator.evaluate(expression)
    print(result)

if __name__ == "__main__":
    main()