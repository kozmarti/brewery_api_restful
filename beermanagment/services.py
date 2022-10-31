from beermanagment.models import Bar, Reference, Stock

def get_full_and_non_full_bars() -> dict:
	bars = {
			"all_stocks" : [],
		    "miss_at_least_one": []
			}
	references = Reference.objects.all().values_list('id', flat=True)
	for bar in Bar.objects.all():
		if references == Stock.objects.filter(bar=bar).values_list('reference', flat=True):
			bars["all_stocks"].append(bar.id)
		else:
			bars["miss_at_least_one"].append(bar.id)
	return bars

