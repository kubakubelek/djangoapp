from django import template
register = template.Library()

@register.filter
def get_vote_value(vote_values, post_id):
    return vote_values.get(post_id, "Brak głosu")