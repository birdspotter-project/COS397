from birdspotter.dataio.models import Dataset


def get_datasets_for_user(user):
	return Dataset.objects.filter(owner_id=user.id).values()
