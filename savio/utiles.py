def mydateconverter(o):
	import datetime
	if isinstance(o, datetime.date):
		return o.__str__()


def convert_date_str(o):
	import datetime
	if isinstance(o, datetime.date):
		x = o.strftime('%Y-%m-%d')
		return x.__str__()


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return floatcomma(obj)


def floatcomma(value):
	orig = force_unicode(value)
	intpart, dec = orig.split(".")
	intpart = intcomma(intpart)
	return ".".join([intpart, dec])

def is_number(x):
	try:
		a = float(x)
	except Exception as e:
		a = 0
	return a
