from types import SimpleNamespace

def dict_to_ns(data):
	if isinstance(data, dict):
		return SimpleNamespace(**{k: dict_to_ns(v) for k, v in data.items()})
	elif isinstance(data, list):
		return [dict_to_ns(i) for i in data]
	return data
