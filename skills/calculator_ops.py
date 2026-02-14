"""
Calculator and Math Operations Skill
"""

import math
from typing import List, Dict, Any, Callable
from core.skill import Skill


class CalculatorSkill(Skill):

    @property
    def name(self) -> str:
        return "calculator_skill"

    # ---------------- TOOL DEFINITIONS ---------------- #

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Perform mathematical calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {"type": "string"}
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "convert_units",
                    "description": "Convert between units",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number"},
                            "from_unit": {"type": "string"},
                            "to_unit": {"type": "string"}
                        },
                        "required": ["value", "from_unit", "to_unit"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "percentage_calculator",
                    "description": "Calculate percentages",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number"},
                            "percentage": {"type": "number"},
                            "operation": {"type": "string"}
                        },
                        "required": ["value", "percentage"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "tip_calculator",
                    "description": "Calculate tip and split bill",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "bill_amount": {"type": "number"},
                            "tip_percentage": {"type": "number"},
                            "split_between": {"type": "integer"}
                        },
                        "required": ["bill_amount"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "calculate": self.calculate,
            "convert_units": self.convert_units,
            "percentage_calculator": self.percentage_calculator,
            "tip_calculator": self.tip_calculator
        }

    # ---------------- CALCULATIONS ---------------- #

    def calculate(self, expression: str) -> dict:
        try:
            expression = expression.strip()

            expression = expression.replace(" plus ", "+")
            expression = expression.replace(" minus ", "-")
            expression = expression.replace(" times ", "*")
            expression = expression.replace(" multiplied by ", "*")
            expression = expression.replace(" divided by ", "/")
            expression = expression.replace(" squared", "**2")
            expression = expression.replace(" cubed", "**3")

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

            result = eval(expression, {"__builtins__": {}}, safe_dict)

            return {"status": "success", "message": f"{expression} = {result}"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def convert_units(self, value: float, from_unit: str, to_unit: str) -> dict:
        try:
            from_unit = from_unit.lower().strip()
            to_unit = to_unit.lower().strip()

            length_to_meters = {
                'm': 1, 'meter': 1,
                'km': 1000, 'kilometer': 1000,
                'cm': 0.01, 'centimeter': 0.01,
                'mile': 1609.34,
            }

            if from_unit in length_to_meters and to_unit in length_to_meters:
                meters = value * length_to_meters[from_unit]
                result = meters / length_to_meters[to_unit]
                return {"status": "success", "message": f"{value} {from_unit} = {result:.2f} {to_unit}"}

            return {"status": "error", "message": "Unsupported unit conversion"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def percentage_calculator(self, value: float, percentage: float, operation: str = "of") -> dict:
        try:
            operation = operation.lower()

            if operation == "of":
                result = (value * percentage) / 100
            elif operation == "increase":
                result = value + (value * percentage / 100)
            elif operation == "decrease":
                result = value - (value * percentage / 100)
            else:
                return {"status": "error", "message": "Invalid operation"}

            return {"status": "success", "message": str(result)}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tip_calculator(self, bill_amount: float, tip_percentage: float = 15, split_between: int = 1) -> dict:
        try:
            tip = bill_amount * (tip_percentage / 100)
            total = bill_amount + tip
            per_person = total / split_between

            return {
                "status": "success",
                "message": f"Total: {total:.2f}, Per person: {per_person:.2f}"
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}


def register():
    """Register the Calculator skill"""
    return CalculatorSkill()
