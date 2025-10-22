"""
Math Tool - Agno compatible calculator
"""
import math


def get_math_tool():
    """Get math calculator tool for Agno"""
    
    def calculator(expression: str) -> str:
        """
        Evaluate mathematical expressions.
        
        Args:
            expression: Mathematical expression like '2 + 2', 'sqrt(16)', 'sin(pi/2)', etc.
        
        Returns:
            Result of the calculation
        """
        try:
            expression = expression.strip()
            
            # Create safe namespace
            safe_dict = {
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'sum': sum,
                'pow': pow,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'log': math.log,
                'log10': math.log10,
                'log2': math.log2,
                'exp': math.exp,
                'floor': math.floor,
                'ceil': math.ceil,
                'degrees': math.degrees,
                'radians': math.radians,
                'factorial': math.factorial,
                'pi': math.pi,
                'e': math.e,
                'tau': math.tau,
                'inf': math.inf,
            }
            
            # Evaluate safely
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            return f"🧮 Result: {expression} = {result}"
        
        except SyntaxError:
            return f"❌ Syntax Error: Invalid expression '{expression}'"
        except NameError:
            return f"❌ Unknown function in '{expression}'. Available: sqrt, sin, cos, tan, log, exp, etc."
        except ZeroDivisionError:
            return "❌ Error: Division by zero"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    return calculator

