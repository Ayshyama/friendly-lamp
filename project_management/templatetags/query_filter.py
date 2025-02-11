from django import template

register = template.Library()


@register.filter(name="is_in1")
def is_in1(var, args):
    if args is None:
        return False
    print(args)
    arg_list = [arg.strip() for arg in args.split(',')]
    return var in arg_list


@register.filter(name="is_not_in")
def is_not_in(var, args):
    print(args)
    if args is None:
        return True
    return not (var in args)
