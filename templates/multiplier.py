from django import template

register = template.Library()

def mul(value,arg):
  try:
    return value * arg
  except(ValueError,TypeError):
    return 0