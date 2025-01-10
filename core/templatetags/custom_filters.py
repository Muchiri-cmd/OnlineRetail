from django import template

# Registering the custom filter
register = template.Library()

@register.filter
def mul(value, arg):
    try:
        if not value or not arg:
            return 0
        
        value = float(value.replace(',', '').strip()) if value.strip() else 0
        arg = float(arg.replace(',', '').strip()) if arg.strip() else 0
        
        return value * arg
    except (ValueError, TypeError) as e:
        print(f"Error: {e}") 
        return 0
      