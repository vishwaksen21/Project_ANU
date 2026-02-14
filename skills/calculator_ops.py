"""
Calculator and Math Operations
"""
import math
import re

def calculate(expression: str) -> dict:
    """
    Perform mathematical calculations.
    
    Args:
        expression: Mathematical expression to evaluate
    
    Returns:
        Calculation result
    """
    try:
        # Clean the expression
        expression = expression.strip()
        
        # Replace common words with operators
        expression = expression.replace(" plus ", "+")
        expression = expression.replace(" minus ", "-")
        expression = expression.replace(" times ", "*")
        expression = expression.replace(" multiplied by ", "*")
        expression = expression.replace(" divided by ", "/")
        expression = expression.replace(" to the power of ", "**")
        expression = expression.replace(" squared", "**2")
        expression = expression.replace(" cubed", "**3")
        
        # Allow safe math functions
        safe_dict = {
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'pi': math.pi,
            'e': math.e,
            'abs': abs,
            'round': round,
            'pow': pow,
        }
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        
        return {"status": "success", "message": f"{expression} = {result}"}
    except Exception as e:
        return {"status": "error", "message": f"Calculation error: {str(e)}"}

def convert_units(value: float, from_unit: str, to_unit: str) -> dict:
    """
    Convert between different units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (km, miles, kg, lbs, celsius, fahrenheit, etc.)
        to_unit: Target unit
    
    Returns:
        Converted value
    """
    try:
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()
        
        # Length conversions
        length_to_meters = {
            'meter': 1, 'meters': 1, 'm': 1,
            'kilometer': 1000, 'kilometers': 1000, 'km': 1000,
            'centimeter': 0.01, 'centimeters': 0.01, 'cm': 0.01,
            'mile': 1609.34, 'miles': 1609.34,
            'foot': 0.3048, 'feet': 0.3048, 'ft': 0.3048,
            'inch': 0.0254, 'inches': 0.0254, 'in': 0.0254,
            'yard': 0.9144, 'yards': 0.9144, 'yd': 0.9144,
        }
        
        # Weight conversions
        weight_to_kg = {
            'kilogram': 1, 'kilograms': 1, 'kg': 1,
            'gram': 0.001, 'grams': 0.001, 'g': 0.001,
            'pound': 0.453592, 'pounds': 0.453592, 'lb': 0.453592, 'lbs': 0.453592,
            'ounce': 0.0283495, 'ounces': 0.0283495, 'oz': 0.0283495,
        }
        
        # Temperature conversions
        if from_unit in ['celsius', 'c'] and to_unit in ['fahrenheit', 'f']:
            result = (value * 9/5) + 32
            return {"status": "success", "message": f"{value}°C = {result:.2f}°F"}
        elif from_unit in ['fahrenheit', 'f'] and to_unit in ['celsius', 'c']:
            result = (value - 32) * 5/9
            return {"status": "success", "message": f"{value}°F = {result:.2f}°C"}
        
        # Length conversions
        if from_unit in length_to_meters and to_unit in length_to_meters:
            meters = value * length_to_meters[from_unit]
            result = meters / length_to_meters[to_unit]
            return {"status": "success", "message": f"{value} {from_unit} = {result:.2f} {to_unit}"}
        
        # Weight conversions
        if from_unit in weight_to_kg and to_unit in weight_to_kg:
            kg = value * weight_to_kg[from_unit]
            result = kg / weight_to_kg[to_unit]
            return {"status": "success", "message": f"{value} {from_unit} = {result:.2f} {to_unit}"}
        
        return {"status": "error", "message": f"Cannot convert from {from_unit} to {to_unit}"}
    except Exception as e:
        return {"status": "error", "message": f"Conversion error: {str(e)}"}

def percentage_calculator(value: float, percentage: float, operation: str = "of") -> dict:
    """
    Calculate percentages.
    
    Args:
        value: Base value
        percentage: Percentage value
        operation: 'of' (what is X% of Y) or 'increase' or 'decrease'
    
    Returns:
        Calculated result
    """
    try:
        operation = operation.lower()
        
        if operation == "of":
            result = (value * percentage) / 100
            return {"status": "success", "message": f"{percentage}% of {value} = {result}"}
        elif operation == "increase":
            result = value + (value * percentage / 100)
            return {"status": "success", "message": f"{value} increased by {percentage}% = {result}"}
        elif operation == "decrease":
            result = value - (value * percentage / 100)
            return {"status": "success", "message": f"{value} decreased by {percentage}% = {result}"}
        else:
            return {"status": "error", "message": "Operation must be 'of', 'increase', or 'decrease'"}
    except Exception as e:
        return {"status": "error", "message": f"Percentage error: {str(e)}"}

def tip_calculator(bill_amount: float, tip_percentage: float = 15, split_between: int = 1) -> dict:
    """
    Calculate tip and split bill.
    
    Args:
        bill_amount: Total bill amount
        tip_percentage: Tip percentage (default: 15%)
        split_between: Number of people to split between
    
    Returns:
        Tip calculation details
    """
    try:
        tip_amount = bill_amount * (tip_percentage / 100)
        total_with_tip = bill_amount + tip_amount
        per_person = total_with_tip / split_between
        
        message = f"Bill: ${bill_amount:.2f}\n"
        message += f"Tip ({tip_percentage}%): ${tip_amount:.2f}\n"
        message += f"Total: ${total_with_tip:.2f}\n"
        if split_between > 1:
            message += f"Per person ({split_between} people): ${per_person:.2f}"
        
        return {"status": "success", "message": message}
    except Exception as e:
        return {"status": "error", "message": f"Tip calculation error: {str(e)}"}

def register():
    """Register calculator skills"""
    from core.skill import Skill
    skill = Skill("calculator")
    skill.register(
        name="calculate",
        func=calculate,
        description="Perform mathematical calculations (supports +, -, *, /, sqrt, sin, cos, etc.)",
        parameters={
            "expression": {"type": "string", "description": "Mathematical expression to evaluate"}
        },
        required=["expression"]
    )
    
    skill.register(
        name="convert_units",
        func=convert_units,
        description="Convert between units (km/miles, kg/lbs, celsius/fahrenheit, etc.)",
        parameters={
            "value": {"type": "number", "description": "Value to convert"},
            "from_unit": {"type": "string", "description": "Source unit"},
            "to_unit": {"type": "string", "description": "Target unit"}
        },
        required=["value", "from_unit", "to_unit"]
    )
    
    skill.register(
        name="percentage_calculator",
        func=percentage_calculator,
        description="Calculate percentages (what is X% of Y, increase/decrease by X%)",
        parameters={
            "value": {"type": "number", "description": "Base value"},
            "percentage": {"type": "number", "description": "Percentage value"},
            "operation": {"type": "string", "description": "Operation: 'of', 'increase', or 'decrease'"}
        },
        required=["value", "percentage"]
    )
    
    skill.register(
        name="tip_calculator",
        func=tip_calculator,
        description="Calculate tip and split bill among people",
        parameters={
            "bill_amount": {"type": "number", "description": "Total bill amount"},
            "tip_percentage": {"type": "number", "description": "Tip percentage (default: 15)"},
            "split_between": {"type": "integer", "description": "Number of people (default: 1)"}
        },
        required=["bill_amount"]
    )

    print("Loaded skill: calculator_skill")
    return skill
