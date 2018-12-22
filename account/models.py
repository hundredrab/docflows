from django.db import models

class Committee(models.Model):
    """Generic committee model.

    Sub-committees will have to be added as separate models and referred to as such.
    """

    name = models.CharField(max_length=30, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.name + '—' + self.description[:20] + '...'

class Role(models.Model):
    """Role and the associated committee relation."""


    name = models.CharField(max_length=30, default='Member')
    committee = models.ForeignKey(Committee, related_name='com_roles', on_delete=models.CASCADE)
    description = models.TextField(default="Describe this role's functionality.")

    def __str__(self):
        return self.name + ' of ' + self.committee.name + ' (' + self.description[:20] + '...)'

    class Meta:
        unique_together = ('committee', 'name')
